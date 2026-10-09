"""
test_scanner_engine.py

Regression tests for ScannerEngine pipeline configuration propagation.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import unittest
from unittest.mock import patch

from backend.scanner_config import ScannerConfig
from backend.scanner_engine import ScannerEngine


class TestScannerEnginePipeline(unittest.TestCase):

    @patch("backend.scanner_engine.PipelineFactory")
    def test_execute_pipeline_propagates_scanner_configuration(
        self,
        mock_factory_class,
    ):
        """
        ScannerEngine must propagate runtime configuration
        into ScannerPipeline.
        """

        mock_pipeline = (
            mock_factory_class.return_value.create.return_value
        )

        expected_result = object()

        mock_pipeline.run.return_value = expected_result

        config = ScannerConfig(
            market="EUR/USD",
            timeframe="M5",
            data_source="TWELVEDATA",
            provider_priority=[
                "TWELVEDATA",
                "API",
            ],
            api_url="https://example.test/api",
            api_key="test-api-key",
        )

        engine = ScannerEngine(config)

        result = engine.execute_pipeline()

        self.assertIs(
            result,
            expected_result,
        )

        mock_factory_class.assert_called_once_with()

        mock_factory_class.return_value.create.assert_called_once_with()

        mock_pipeline.run.assert_called_once_with(
            "EUR/USD",
            "M5",
            metadata={
                "data_source": "TWELVEDATA",
                "provider_priority": [
                    "TWELVEDATA",
                    "API",
                ],
            },
            provider_config=config,
        )

    @patch("backend.scanner_engine.PipelineFactory")
    def test_execute_pipeline_allows_runtime_market_and_timeframe_override(
        self,
        mock_factory_class,
    ):
        """
        Runtime market/timeframe overrides must be used without
        changing the configured scanner values.
        """

        mock_pipeline = (
            mock_factory_class.return_value.create.return_value
        )

        expected_result = object()

        mock_pipeline.run.return_value = expected_result

        config = ScannerConfig(
            market="EUR/USD",
            timeframe="M5",
            data_source="TWELVEDATA",
            provider_priority=[
                "TWELVEDATA",
                "API",
            ],
            api_url="https://example.test/api",
            api_key="test-api-key",
        )

        engine = ScannerEngine(config)

        result = engine.execute_pipeline(
            market="GBP/USD",
            timeframe="M15",
        )

        self.assertIs(
            result,
            expected_result,
        )

        mock_pipeline.run.assert_called_once_with(
            "GBP/USD",
            "M15",
            metadata={
                "data_source": "TWELVEDATA",
                "provider_priority": [
                    "TWELVEDATA",
                    "API",
                ],
            },
            provider_config=config,
        )

        self.assertEqual(
            engine.config.market,
            "EUR/USD",
        )

        self.assertEqual(
            engine.config.timeframe,
            "M5",
        )


if __name__ == "__main__":
    unittest.main()
