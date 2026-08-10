"""
provider_health_manager.py

Manages health checks for all registered market data providers.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.provider_health import ProviderHealth


class ProviderHealthManager:
    """
    Manages ProviderHealth instances for registered providers.
    """

    def __init__(self, provider_manager):

        self.provider_manager = provider_manager
        self._health = {}

    # ==================================================
    # Get Provider Health
    # ==================================================

    def get_health(
        self,
        provider_name,
        config=None,
    ):
        """
        Return the ProviderHealth object for a provider.

        If config is supplied, it is used to create the
        provider instance used by the health checker.
        """

        provider_name = provider_name.upper()

        provider_class = self.provider_manager.get_provider(
            provider_name
        )

        if provider_class is None:
            return None

        if provider_name not in self._health:

            provider = self._create_provider(
                provider_name,
                config,
            )

            if provider is None:
                return None

            self._health[provider_name] = ProviderHealth(
                provider
            )

        return self._health[provider_name]

    # ==================================================
    # Create Provider
    # ==================================================

    def _create_provider(
        self,
        provider_name,
        config=None,
    ):
        """
        Create a provider instance for health checking.

        Uses the real ScannerConfig when supplied.
        """

        provider_class = self.provider_manager.get_provider(
            provider_name
        )

        if provider_class is None:
            return None

        if config is None:

            config = type(
                "HealthConfig",
                (),
                {
                    "market": "UNKNOWN",
                    "timeframe": "UNKNOWN",
                    "data_source": provider_name,
                    "api_url": None,
                    "api_key": None,
                    "provider_priority": [
                        provider_name
                    ],
                },
            )()

        else:

            config.data_source = provider_name

        try:

            return provider_class(config)

        except Exception:

            return None

    # ==================================================
    # Check Provider
    # ==================================================

    def check(
        self,
        provider_name,
        config=None,
    ):
        """
        Perform a health check for one provider.
        """

        health = self.get_health(
            provider_name,
            config,
        )

        if health is None:
            return False

        return health.check()

    # ==================================================
    # Check All Providers
    # ==================================================

    def check_all(self, config=None):
        """
        Perform health checks for all registered providers.
        """

        results = {}

        for provider_name in (
            self.provider_manager.registered_providers()
        ):

            health = self.get_health(
                provider_name,
                config,
            )

            if health is None:

                results[provider_name] = False

                continue

            results[provider_name] = health.check()

        return results

    # ==================================================
    # Is Healthy
    # ==================================================

    def is_healthy(
        self,
        provider_name,
        config=None,
    ):
        """
        Return whether a provider is currently healthy.
        """

        health = self.get_health(
            provider_name,
            config,
        )

        if health is None:
            return False

        return health.healthy

    # ==================================================
    # Report
    # ==================================================

    def report(self):
        """
        Return health information for all
        providers that have been checked.
        """

        report = {}

        for provider_name, health in self._health.items():

            report[provider_name] = health.report()

        return report
