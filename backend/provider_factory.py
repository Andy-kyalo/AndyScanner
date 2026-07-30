"""
provider_factory.py

Factory responsible for creating market data providers.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.provider_manager import ProviderManager
from backend.provider_exceptions import (
    ProviderNotFoundError,
)


class ProviderFactory:
    """
    Creates provider instances using the ProviderManager.
    """

    def __init__(self, manager: ProviderManager):

        self.manager = manager

    # ==================================================
    # Create Provider
    # ==================================================

    def create(self, config):
        """
        Create a provider from scanner configuration.
        """

        provider_name = config.data_source.upper()

        if not self.manager.provider_exists(provider_name):

            available = ", ".join(self.manager.providers())

            raise ProviderNotFoundError(
                f"Provider '{provider_name}' is not registered. "
                f"Available providers: {available}"
            )

        return self.manager.create(config)