"""
test_provider_stage.py

Integration tests for ProviderStage failover,
health, retry, timeout, and recovery behavior.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import unittest
from unittest.mock import Mock, patch

from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.stages.provider_stage import ProviderStage
from backend.provider_exceptions import ProviderConnectionError
from backend.provider_timeout import ProviderTimeout


class FakeProvider:
    name = "FakeProvider"

    def __init__(self, config):
        self.config = config
        self.probe_error = None

    def probe(self):
        return True

    def load(self, symbol):
        return [
            {
                "time": "2026-01-01 10:00:00",
                "open": 1.1,
                "high": 1.2,
                "low": 1.0,
                "close": 1.15,
                "volume": 100,
            }
        ]


class FailingProvider(FakeProvider):
    name = "FailingProvider"

    def load(self, symbol):
        raise ProviderConnectionError(
            "simulated provider connection failure"
        )


class TestProviderStage(unittest.TestCase):

    def make_context(self):
        context = PipelineContext()
        context.start("EURUSD", "M5")

        context.set_metadata(
            "data_source",
            "FAKE",
        )

        context.set_metadata(
            "provider_priority",
            ["FAKE"],
        )

        return context

    def test_custom_provider_config_is_used_without_metadata_credentials(self):
        from backend.scanner_config import ScannerConfig

        context = self.make_context()
        custom_config = ScannerConfig(
            market="EURUSD",
            timeframe="M5",
            data_source="FAKE",
            api_url="https://example.test/custom",
            api_key="test-api-key",
            provider_priority=["FAKE"],
        )
        context.provider_config = custom_config

        self.assertNotIn("api_key", context.metadata)
        self.assertNotIn("api_url", context.metadata)

        captured = {}

        class CapturingProvider(FakeProvider):
            def __init__(self, config):
                super().__init__(config)
                captured["api_url"] = config.api_url
                captured["api_key"] = config.api_key

        manager = Mock()
        manager.provider_exists.return_value = True
        manager.get_provider.return_value = CapturingProvider
        manager.create_provider.side_effect = (
            lambda name, config: CapturingProvider(config)
        )

        with patch(
            "backend.pipeline.stages.provider_stage.register_providers",
            return_value=manager,
        ), patch(
            "backend.pipeline.stages.provider_stage.SymbolResolver.resolve"
        ) as resolve:
            resolution = Mock()
            resolution.canonical = "EURUSD"
            resolution.provider = "FAKE"
            resolution.symbol = "EURUSD"
            resolution.supported = True
            resolve.return_value = resolution

            ProviderStage().run(context)

        self.assertEqual(
            captured["api_url"],
            "https://example.test/custom",
        )
        self.assertEqual(
            captured["api_key"],
            "test-api-key",
        )

    def test_healthy_provider_returns_candles(self):
        context = self.make_context()

        manager = Mock()
        manager.provider_exists.return_value = True
        manager.get_provider.return_value = FakeProvider
        manager.create_provider.return_value = FakeProvider(
            context
        )

        with patch(
            "backend.pipeline.stages.provider_stage.register_providers",
            return_value=manager,
        ), patch(
            "backend.pipeline.stages.provider_stage.SymbolResolver.resolve"
        ) as resolve:

            resolution = Mock()
            resolution.canonical = "EURUSD"
            resolution.provider = "FAKE"
            resolution.symbol = "EURUSD"
            resolution.supported = True

            resolve.return_value = resolution

            result = ProviderStage().run(context)

        self.assertIsNotNone(result.candles)
        self.assertEqual(
            result.get_metadata("selected_provider"),
            "FakeProvider",
        )
        self.assertFalse(
            result.get_metadata("failover_used")
        )

    def test_provider_load_failure_enters_cooldown(self):
        context = self.make_context()

        manager = Mock()
        manager.provider_exists.return_value = True
        manager.get_provider.return_value = FailingProvider
        manager.create_provider.return_value = FailingProvider(
            context
        )

        with patch(
            "backend.pipeline.stages.provider_stage.register_providers",
            return_value=manager,
        ), patch(
            "backend.pipeline.stages.provider_stage.SymbolResolver.resolve"
        ) as resolve:

            resolution = Mock()
            resolution.canonical = "EURUSD"
            resolution.provider = "FAKE"
            resolution.symbol = "EURUSD"
            resolution.supported = True

            resolve.return_value = resolution

            with self.assertRaises(
                ProviderConnectionError
            ):
                ProviderStage().run(context)

        recovery = context.get_metadata(
            "provider_recovery"
        )

        self.assertEqual(
            recovery["FAKE"]["status"],
            "COOLDOWN",
        )

        failures = context.get_metadata(
            "provider_failures"
        )

        self.assertTrue(failures)

    def test_failed_provider_fails_over_to_next_provider(self):
        context = self.make_context()

        context = self.make_context()

        context.set_metadata(
            "data_source",
            "FAILING",
          )

        context.set_metadata(
             "provider_priority",
            ["FAILING", "FAKE"],
         )

        failing = FailingProvider(context)
        healthy = FakeProvider(context)

        manager = Mock()

        def provider_exists(name):
            return name in {
                "FAILING",
                "FAKE",
            }

        def get_provider(name):
            if name == "FAILING":
                return FailingProvider
            return FakeProvider

        def create_provider(name, config):
            if name == "FAILING":
                return failing
            return healthy

        manager.provider_exists.side_effect = provider_exists
        manager.get_provider.side_effect = get_provider
        manager.create_provider.side_effect = create_provider

        def resolve_provider(market, provider):
            resolution = Mock()
            resolution.canonical = "EURUSD"
            resolution.provider = provider
            resolution.symbol = "EURUSD"
            resolution.supported = True
            return resolution

        with patch(
            "backend.pipeline.stages.provider_stage.register_providers",
            return_value=manager,
        ), patch(
            "backend.pipeline.stages.provider_stage.SymbolResolver.resolve",
            side_effect=resolve_provider,
        ):

            result = ProviderStage().run(context)

        self.assertEqual(
            result.get_metadata("selected_provider"),
            "FakeProvider",
        )

        self.assertTrue(
            result.get_metadata("failover_used")
        )

        attempts = result.get_metadata(
            "provider_attempts"
        )

        self.assertEqual(
            attempts,
            ["FAILING", "FAKE"],
        )

    def test_provider_in_cooldown_is_skipped(self):
        context = self.make_context()

        manager = Mock()
        manager.provider_exists.return_value = True
        manager.get_provider.return_value = FakeProvider

        stage = ProviderStage()

        stage.recovery.record_failure(
            "FAKE"
        )

        with patch(
            "backend.pipeline.stages.provider_stage.register_providers",
            return_value=manager,
        ), patch(
            "backend.pipeline.stages.provider_stage.SymbolResolver.resolve"
        ) as resolve:

            resolution = Mock()
            resolution.canonical = "EURUSD"
            resolution.provider = "FAKE"
            resolution.symbol = "EURUSD"
            resolution.supported = True

            resolve.return_value = resolution

            with self.assertRaises(RuntimeError):
                stage.run(context)

        manager.create_provider.assert_not_called()

        recovery = context.get_metadata(
            "provider_recovery"
        )

        self.assertEqual(
            recovery["FAKE"]["status"],
            "COOLDOWN",
        )

    def test_unsupported_market_does_not_enter_cooldown(self):
        context = self.make_context()

        manager = Mock()
        manager.provider_exists.return_value = True

        stage = ProviderStage()

        with patch(
            "backend.pipeline.stages.provider_stage.register_providers",
            return_value=manager,
        ), patch(
            "backend.pipeline.stages.provider_stage.SymbolResolver.resolve"
        ) as resolve:

            resolution = Mock()
            resolution.canonical = "EURUSD"
            resolution.provider = "FAKE"
            resolution.symbol = None
            resolution.supported = False

            resolve.return_value = resolution

            with self.assertRaises(RuntimeError):
                stage.run(context)

        manager.create_provider.assert_not_called()

        recovery = context.get_metadata(
            "provider_recovery"
        )

        self.assertEqual(
            recovery["FAKE"]["status"],
            "UNSUPPORTED_MARKET",
        )

        self.assertFalse(
            stage.recovery.is_in_cooldown(
                "FAKE"
            )
        )


if __name__ == "__main__":
    unittest.main()
