"""
provider_manager.py

Professional Provider Manager for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""

from backend.provider_exceptions import ProviderNotFoundError


class ProviderManager:
    """
    Manages all available market data providers.
    """

    def __init__(self):
        self._providers = {}
        self._active_provider = None

        # Provider metrics
        self._total_requests = 0
        self._successful_requests = 0
        self._failed_requests = 0

    # ==================================================
    # Register Provider
    # ==================================================

    def register(self, name, provider_class):
        """
        Register a provider class.
        """

        name = name.upper()

        self._providers[name] = provider_class

        if self._active_provider is None:
            self._active_provider = name

    # ==================================================
    # Provider Exists
    # ==================================================

    def provider_exists(self, name):
        """
        Check whether a provider is already registered.
        """

        return name.upper() in self._providers

    # ==================================================
    # Get Provider Class
    # ==================================================

    def get_provider(self, name):
        """
        Return a registered provider class.
        """

        return self._providers.get(name.upper())

    # ==================================================
    # Create Provider
    # ==================================================

    def create(self, config):
        """
        Create an instance of the configured provider.

        Providers are registered as classes and are instantiated
        with the scanner configuration.
        """

        provider_name = config.data_source.upper()

        provider_class = self.get_provider(provider_name)

        if provider_class is None:

            available = ", ".join(
                self.registered_providers()
            )

            raise ProviderNotFoundError(
                f"Provider '{provider_name}' is not registered. "
                f"Available providers: {available}"
            )

        self._total_requests += 1

        try:

            provider = provider_class(config)

            return provider

        except Exception:

            self._failed_requests += 1

            raise

    # ==================================================
    # Active Provider
    # ==================================================

    def get_active_provider_name(self):
        """
        Return the active provider name.
        """

        return self._active_provider

    def get_active_provider(self):
        """
        Return the active provider class.
        """

        if self._active_provider is None:
            return None

        return self._providers[self._active_provider]

    # ==================================================
    # Set Active Provider
    # ==================================================

    def set_active_provider(self, name):
        """
        Change the active provider.
        """

        name = name.upper()

        if not self.provider_exists(name):

            raise ValueError(
                f"Provider '{name}' is not registered."
            )

        self._active_provider = name

    # ==================================================
    # Registered Providers
    # ==================================================

    def registered_providers(self):
        """
        Return a list of registered providers.
        """

        return list(self._providers.keys())

    # ==================================================
    # Provider Alias
    # ==================================================

    def providers(self):
        """
        Return registered provider names.

        Compatibility method used by ProviderFactory.
        """

        return self.registered_providers()

    # ==================================================
    # Total Providers
    # ==================================================

    def total_providers(self):
        """
        Return total number of registered providers.
        """

        return len(self._providers)

    # ==================================================
    # Record Success
    # ==================================================

    def record_success(self):
        """
        Record a successful provider operation.
        """

        self._successful_requests += 1

    # ==================================================
    # Record Failure
    # ==================================================

    def record_failure(self):
        """
        Record a failed provider operation.
        """

        self._failed_requests += 1

    # ==================================================
    # Metrics
    # ==================================================

    def metrics_report(self):
        """
        Return provider performance metrics.
        """

        total = self._total_requests

        if total > 0:
            success_rate = (
                self._successful_requests / total
            ) * 100
        else:
            success_rate = 0.0

        return {
            "total_requests": total,
            "successful_requests": self._successful_requests,
            "failed_requests": self._failed_requests,
            "success_rate": round(success_rate, 2),
        }