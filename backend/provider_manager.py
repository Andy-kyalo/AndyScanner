"""
provider_manager.py

Professional Provider Manager for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""


class ProviderManager:
    """
    Manages all available market data providers.
    """

    def __init__(self):
        self._providers = {}
        self._active_provider = None

    # ==================================================
    # Register Provider
    # ==================================================

    def register(self, name, provider_class):
        """
        Register a provider class.
        """

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

        return name in self._providers

    # ==================================================
    # Get Provider Class
    # ==================================================

    def get_provider(self, name):
        """
        Return a registered provider class.
        """

        return self._providers.get(name)

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
    # Total Providers
    # ==================================================

    def total_providers(self):
        """
        Return total registered providers.
        """

        return len(self._providers)