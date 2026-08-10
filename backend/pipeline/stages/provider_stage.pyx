"""
provider_stage.py

Provider Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_stage import PipelineStage

from backend.provider_retry import ProviderRetry
from backend.provider_timeout import ProviderTimeout

from backend.provider_health_manager import (
    ProviderHealthManager,
)

from backend.register_providers import register_providers
from backend.scanner_config import ScannerConfig


class ProviderStage(PipelineStage):
    """
    Responsible for obtaining market data
    from the configured provider.

    Supports provider health checks and
    provider failover using the configured
    provider priority.
    """

    def __init__(self):

        super().__init__("Provider Stage")

    # ==================================================
    # Execute
    # ==================================================

    def execute(self, context):

        provider_manager = register_providers()

        data_source = context.get_metadata(
            "data_source",
            "CSV",
        ).upper()

        configured_priority = context.get_metadata(
            "provider_priority",
            [
                "CSV",
                "API",
                "MT5",
            ],
        )

        # Put the requested provider first.
        provider_priority = [
            data_source
        ]

        for provider_name in configured_priority:

            provider_name = provider_name.upper()

            if provider_name not in provider_priority:

                provider_priority.append(
                    provider_name
                )

        config = ScannerConfig(
            market=context.market,
            timeframe=context.timeframe,
            data_source=data_source,
            api_url=context.get_metadata(
                "api_url"
            ),
            api_key=context.get_metadata(
                "api_key"
            ),
            provider_priority=provider_priority,
        )

        attempts = []
        failures = []

        selected_provider = None
        candles = None
        last_exception = None

        # ==================================================
        # Provider Health Manager
        # ==================================================

        health_manager = ProviderHealthManager(
            provider_manager
        )

        health_results = {}

        # ==================================================
        # Provider Failover
        # ==================================================

        for provider_name in provider_priority:

            if not provider_manager.provider_exists(
                provider_name
            ):

                failures.append(
                    {
                        "provider": provider_name,
                        "error": (
                            "Provider is not registered."
                        ),
                    }
                )

                health_results[
                    provider_name
                ] = False

                continue

            # --------------------------------------------------
            # Health Check
            # --------------------------------------------------
            attempts.append(
                provider_name
            )
            config.data_source = provider_name

            healthy = health_manager.check(
                provider_name,
                config,
            )

            health_results[
                provider_name
            ] = healthy

            if not healthy:

                failures.append(
                    {
                        "provider": provider_name,
                        "error": (
                            "Provider failed health check."
                        ),
                    }
                )

                continue

            # --------------------------------------------------
            # Provider Attempt
            # --------------------------------------------------

            attempts.append(
                provider_name
            )

            try:

                provider = (
                    provider_manager.create_provider(
                        provider_name,
                        config,
                    )
                )

                timeout = ProviderTimeout(
                    timeout=10.0,
                )

                retry = ProviderRetry(
                    retries=3,
                    delay=1.0,
                )

                candles = retry.execute(
                    lambda: timeout.execute(
                        provider.load
                    )
                )

                # Provider succeeded.
                selected_provider = provider

                provider_manager.record_success()

                break

            except Exception as error:

                last_exception = error

                provider_manager.record_failure()

                failures.append(
                    {
                        "provider": provider_name,
                        "error": str(error),
                    }
                )

        # ==================================================
        # All Providers Failed
        # ==================================================

        if selected_provider is None:

            context.set_metadata(
                "provider_attempts",
                attempts,
            )

            context.set_metadata(
                "provider_failures",
                failures,
            )

            context.set_metadata(
                "selected_provider",
                None,
            )

            context.set_metadata(
                "provider_health",
                health_results,
            )

            context.set_metadata(
                "health_checked",
                True,
            )

            context.set_metadata(
                "failover_used",
                len(attempts) > 1,
            )

            if last_exception is not None:

                raise last_exception

            raise RuntimeError(
                "No healthy registered provider "
                "could be used."
            )

        # ==================================================
        # Store Successful Provider
        # ==================================================

        context.provider = selected_provider

        context.provider_manager = provider_manager

        context.candles = candles

        context.set_metadata(
            "provider",
            selected_provider.name,
        )

        context.set_metadata(
            "selected_provider",
            selected_provider.name,
        )

        context.set_metadata(
            "provider_attempts",
            attempts,
        )

        context.set_metadata(
            "provider_failures",
            failures,
        )

        context.set_metadata(
            "provider_priority",
            provider_priority,
        )

        context.set_metadata(
            "provider_health",
            health_results,
        )

        context.set_metadata(
            "health_checked",
            True,
        )

        context.set_metadata(
            "failover_used",
            (
                attempts[0]
                != selected_provider.name.replace(
                    "Provider",
                    ""
                )
                if attempts
                else False
            ),
        )

        context.set_metadata(
            "candles",
            len(candles),
        )

        return context
