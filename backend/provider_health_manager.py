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

    def get_health(self, provider_name):
        """
        Return the ProviderHealth object for a provider.

        Creates the health object if it does not already exist.
        """

        provider_name = provider_name.upper()

        provider_class = self.provider_manager.get_provider(
            provider_name
        )

        if provider_class is None:
            return None

        if provider_name not in self._health:

            # ProviderHealth requires a provider instance.
            provider = self._create_provider(
                provider_name
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

    def _create_provider(self, provider_name):
        """
        Create a provider instance for health checking.

        Uses the registered provider class with a minimal
        configuration object when possible.
        """

        provider_class = self.provider_manager.get_provider(
            provider_name
        )

        if provider_class is None:
            return None

        try:

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

            return provider_class(config)

        except Exception:
            return None

    # ==================================================
    # Check Provider
    # ==================================================

    def check(self, provider_name):
        """
        Perform a health check for one provider.
        """

        health = self.get_health(provider_name)

        if health is None:
            return False

        return health.check()

    # ==================================================
    # Check All Providers
    # ==================================================

    def check_all(self):
        """
        Perform health checks for all registered providers.

        Returns:
            dict containing provider health status.
        """

        results = {}

        for provider_name in (
            self.provider_manager.registered_providers()
        ):

            health = self.get_health(provider_name)

            if health is None:
                results[provider_name] = False
                continue

            results[provider_name] = health.check()

        return results

    # ==================================================
    # Is Healthy
    # ==================================================

    def is_healthy(self, provider_name):
        """
        Return whether a provider is currently healthy.
        """

        health = self.get_health(provider_name)

        if health is None:
            return False

        return health.healthy

    # ==================================================
    # Report
    # ==================================================

    def report(self):
        """
        Return health information for all managed providers.
        """

        report = {}

        for provider_name, health in self._health.items():

            report[provider_name] = health.report()

        return report
