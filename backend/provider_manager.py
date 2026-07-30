"""
provider_manager.py

Central manager for market data providers.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.provider_registry import ProviderRegistry
from backend.provider_health import ProviderHealth
from backend.provider_metrics import ProviderMetrics
from backend.provider_exceptions import (
    ProviderNotFoundError,
)


class ProviderManager:
    """
    Coordinates provider registration,
    provider creation,
    provider failover,
    health monitoring,
    and performance metrics.
    """

    def __init__(self):

        self.registry = ProviderRegistry()
        self.metrics = ProviderMetrics()

    # ==================================================
    # Registration
    # ==================================================

    def register(
        self,
        name,
        provider_class,
    ):

        self.registry.register(
            name,
            provider_class,
        )

    # ==================================================
    # Provider Creation (Automatic Failover)
    # ==================================================

    def create(self, config):
        """
        Create the first healthy provider from the
        configured provider priority list.
        """

        last_error = None

        for provider_name in config.provider_priority:

            provider_class = self.registry.get(provider_name)

            if provider_class is None:
                continue

            try:

                provider = provider_class(config)

                health = ProviderHealth(provider)

                if health.check():

                    return provider

            except Exception as error:

                last_error = error
                continue

        if last_error:

            raise RuntimeError(
                f"No available provider. Last error: {last_error}"
            )

        raise ProviderNotFoundError(
            "No registered providers are available."
        )

    # ==================================================
    # Health
    # ==================================================

    def health(self, provider):

        return ProviderHealth(provider)

    # ==================================================
    # Metrics
    # ==================================================

    def record_success(self):

        self.metrics.record_success()

    def record_failure(self):

        self.metrics.record_failure()

    def metrics_report(self):

        return self.metrics.report()

    # ==================================================
    # Registry Information
    # ==================================================

    def providers(self):

        return self.registry.names()

    def provider_exists(
        self,
        name,
    ):

        return self.registry.exists(name)

    def provider_count(self):

        return self.registry.count()