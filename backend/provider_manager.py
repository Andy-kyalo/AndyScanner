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
    creation, health monitoring,
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
    # Provider Creation
    # ==================================================

    def create(
        self,
        name,
        config,
    ):
        """
        Create a provider instance.
        """

        provider_class = self.registry.get(name)

        if provider_class is None:

            raise ProviderNotFoundError(
                f"Provider '{name}' is not registered."
            )

        return provider_class(config)

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