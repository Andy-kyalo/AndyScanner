"""
provider_stage.py

Provider Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_stage import PipelineStage
from backend.provider_retry import ProviderRetry
from backend.provider_timeout import ProviderTimeout
from backend.provider_recovery import ProviderRecovery
from backend.provider_health_manager import ProviderHealthManager
from backend.register_providers import register_providers
from backend.scanner_config import ScannerConfig
from backend.symbol_mapping.symbol_resolver import SymbolResolver
from config.config import Config


class ProviderStage(PipelineStage):
    """
    Responsible for obtaining market data
    from the configured provider.

    Supports:

    - canonical symbol resolution
    - provider support detection
    - provider health checks
    - provider recovery
    - provider cooldown
    - provider retry
    - provider timeout
    - provider failover
    """

    def __init__(self):
        super().__init__("Provider Stage")

        self.recovery = ProviderRecovery(
            cooldown=60.0,
        )

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
                "TWELVEDATA",
                "API",
                "CSV",
                "MT5",
            ],
        )

        # Requested provider always gets first priority.
        provider_priority = [data_source]

        for provider_name in configured_priority:


            # --------------------------------------------------
            # Provider Registration
            # --------------------------------------------------

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
                "api_url",
                Config.API_URL,
            ),
            api_key=context.get_metadata(
                "api_key",
                Config.API_KEY,
            ),
            provider_priority=provider_priority,
        )

        attempts = []
        failures = []

        selected_provider = None
        candles = None
        last_exception = None

        # ==================================================
        # Provider Health
        # ==================================================

        health_manager = ProviderHealthManager(
            provider_manager
        )

        health_results = {}
        recovery_results = {}
        symbol_results = {}

        # ==================================================
        # Provider Failover
        # ==================================================

        for provider_name in provider_priority:

            # --------------------------------------------------
            # Provider Registration
            # --------------------------------------------------

            if not provider_manager.provider_exists(
                provider_name
            ):

                # Provider is not registered — record failure
                # without attempting to fetch health.
                health_error = "Provider is not registered."

                failures.append(
                    {
                        "provider": provider_name,
                        "error": health_error,
                    }
                )

                health_results[
                    provider_name
                ] = False

                recovery_results[
                    provider_name
                ] = {
                    "status": "UNREGISTERED",
                }

                symbol_results[
                    provider_name
                ] = {
                    "canonical": context.market,
                    "symbol": None,
                    "supported": False,
                }

                continue

            # --------------------------------------------------
            # Canonical Symbol Resolution
            # --------------------------------------------------

            resolution = SymbolResolver.resolve(
                context.market,
                provider_name,
            )

            symbol_results[
                provider_name
            ] = {
                "canonical": resolution.canonical,
                "provider": resolution.provider,
                "symbol": resolution.symbol,
                "supported": resolution.supported,
            }

            if not resolution.supported:

                # Provider was considered in the failover sequence,
                # but the requested canonical market is unsupported.
                attempts.append(provider_name)

                failures.append(
                    {
                        "provider": provider_name,
                        "error": (
                            f"Market '{resolution.canonical}' "
                            f"is not supported by provider "
                            f"'{resolution.provider}'."
                        ),
                    }
                )

                health_results[
                    provider_name
                ] = False

                recovery_results[
                    provider_name
                ] = {
                    "status": "UNSUPPORTED_MARKET",
                    "cooldown_remaining": 0.0,
                }

                # Unsupported market is not a provider health failure.
                # Do not put it into ProviderRecovery cooldown.
                continue

            # --------------------------------------------------
            # Recovery / Cooldown
            # --------------------------------------------------

            if self.recovery.is_in_cooldown(
                provider_name
            ):

                remaining = (
                    self.recovery.cooldown_remaining(
                        provider_name
                    )
                )

                recovery_results[
                    provider_name
                ] = {
                    "status": "COOLDOWN",
                    "cooldown_remaining": remaining,
                }

                health_results[
                    provider_name
                ] = False

                failures.append(
                    {
                        "provider": provider_name,
                        "error": (
                            "Provider is in cooldown."
                        ),
                    }
                )

                continue

            # --------------------------------------------------
            # Recovery Attempt
            # --------------------------------------------------

            self.recovery.record_recovery_attempt(
                provider_name
            )

            recovery_results[
                provider_name
            ] = {
                "status": "AVAILABLE",
                "cooldown_remaining": 0.0,
            }

            # This provider is genuinely being tested.
            attempts.append(provider_name)

            # --------------------------------------------------
            # Health Check
            # --------------------------------------------------

            config.data_source = provider_name

            healthy = health_manager.check(
                provider_name,
                config,
            )

            health_results[
                provider_name
            ] = healthy

            if not healthy:

                self.recovery.record_failure(
                    provider_name
                )

                recovery_results[
                    provider_name
                ] = self.recovery.info(
                    provider_name
                )

                health = health_manager.get_health(
                    provider_name,
                    config,
                )

                health_error = None

                if health is not None:
                    health_error = health.last_error

                failures.append(
                    {
                        "provider": provider_name,
                        "error": (
                            health_error
                            or "Provider failed health check."
                        ),
                    }
                )

                continue

            # --------------------------------------------------
            # Provider Load
            # --------------------------------------------------
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
                        lambda: provider.load(
                            symbol=resolution.symbol
                        )
                    )
                )

                if not candles:
                    raise RuntimeError(
                        f"Provider '{provider_name}' "
                        "returned no candles."
                    )

                # --------------------------------------------------
                # Success
                # --------------------------------------------------
                selected_provider = provider

                provider_manager.record_success()

                self.recovery.record_recovery(
                    provider_name
                )

                recovery_results[
                    provider_name
                ] = {
                    "status": "AVAILABLE",
                    "cooldown_remaining": 0.0,
                }

                break

            except Exception as error:

                last_exception = error

                provider_manager.record_failure()

                self.recovery.record_failure(
                    provider_name
                )

                # --------------------------------------------------
                # Classify actual provider load failure
                # --------------------------------------------------
                error_type = type(error).__name__
                error_message = str(error)

                failure_category = "PROVIDER_ERROR"

                if error_type == "ProviderMarketUnsupportedError":
                    failure_category = "MARKET_UNSUPPORTED"

                elif error_type == "ProviderPlanRestrictedError":
                    failure_category = "PLAN_RESTRICTED"

                elif error_type == "ProviderRateLimitError":
                    failure_category = "RATE_LIMITED"

                elif error_type == "ProviderAuthenticationError":
                    failure_category = "AUTHENTICATION_ERROR"

                elif error_type == "ProviderTimeoutError":
                    failure_category = "TIMEOUT"

                elif error_type == "ProviderConnectionError":
                    failure_category = "CONNECTION_ERROR"

                elif error_type == "ProviderUnavailableError":
                    failure_category = "PROVIDER_UNAVAILABLE"

                elif error_type == "ProviderDataError":
                    failure_category = "DATA_ERROR"

                elif error_type == "ProviderConfigurationError":
                    failure_category = "CONFIGURATION_ERROR"

                # --------------------------------------------------
                # Record actual failure
                # --------------------------------------------------
                failures.append(
                    {
                        "provider": provider_name,
                        "error_type": error_type,
                        "category": failure_category,
                        "error": error_message,
                    }
                )

                recovery_results[
                    provider_name
                ] = {
                    "status": "COOLDOWN",
                    "cooldown_remaining":
                        self.recovery.cooldown_remaining(
                            provider_name
                        ),
                }

                # --------------------------------------------------
                # IMPORTANT:
                # Continue failover to the next provider.
                # --------------------------------------------------
                continue

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
                "provider_recovery",
                recovery_results,
            )

            context.set_metadata(
                "provider_symbols",
                symbol_results,
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
                "No supported and healthy registered "
                "provider could be used."
            )

        # ==================================================
        # Store Successful Provider
        # ==================================================

        context.provider = selected_provider
        context.provider_manager = provider_manager
        context.candles = candles

        selected_resolution = SymbolResolver.resolve(
            context.market,
            selected_provider.name.replace(
                "Provider",
                "",
            ),
        )

        context.set_metadata(
            "provider",
            selected_provider.name,
        )

        context.set_metadata(
            "selected_provider",
            selected_provider.name,
        )

        context.set_metadata(
            "provider_symbol",
            selected_resolution.symbol,
        )

        context.set_metadata(
            "canonical_market",
            selected_resolution.canonical,
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
            "provider_recovery",
            recovery_results,
        )

        context.set_metadata(
            "provider_symbols",
            symbol_results,
        )

        context.set_metadata(
            "health_checked",
            True,
        )

        selected_name = selected_provider.name.replace(
            "Provider",
            "",
        ).upper()

        context.set_metadata(
            "failover_used",
            attempts[0].upper() != selected_name
            if attempts
            else False,
        )

        context.set_metadata(
            "candles",
            candles,
        )
        return context
