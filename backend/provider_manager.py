"""
provider_manager.py

Central manager for market data providers.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.logger import Logger
from backend.provider_registry import ProviderRegistry
from backend.provider_health import ProviderHealth
from backend.provider_metrics import ProviderMetrics


class ProviderManager:
    """
    Coordinates provider registration,
    creation, health monitoring,
    metrics and provider selection.
    """

    def __init__(self):

        self.logger = Logger()

        self.registry = ProviderRegistry()
        self.metrics = ProviderMetrics()

    # ==================================================
    # Registry
    # ==================================================

    def register(self, name: str, provider_class) -> None:
        """
        Register a provider.
        """

        self.registry.register(name, provider_class)

        self.logger.info(
            "ProviderManager",
            f"Registered provider: {name.upper()}"
        )

    # ==================================================
    # Provider Creation
    # ==================================================

    def create(self, name: str, config):
        """
        Create provider instance.
        """

        provider_class = self.registry.get(name)

        if provider_class is None:

            raise ValueError(
                f"Provider '{name}' is not registered."
            )

        provider = provider_class(config)

        self.logger.info(
            "ProviderManager",
            f"Created provider: {name.upper()}"
        )

        return provider

    # ==================================================
    # Health
    # ==================================================

    def health(self, provider) -> ProviderHealth:
        """
        Return provider health checker.
        """

        return ProviderHealth(provider)

    def is_healthy(self, provider) -> bool:
        """
        Check provider health.
        """

        return self.health(provider).check()

    # ==================================================
    # Metrics
    # ==================================================

    def metrics_report(self) -> dict:
        """
        Return provider metrics.
        """

        return self.metrics.report()

    # ==================================================
    # Registry Information
    # ==================================================

    def providers(self) -> list[str]:
        """
        Return registered providers.
        """

        return self.registry.names()

    # ==================================================
    # Future Failover
    # ==================================================

    def get_best_provider(self, config):
        """
        Reserved for automatic provider
        failover in future versions.
        """

        return self.create(
            config.data_source,
            config,
        )