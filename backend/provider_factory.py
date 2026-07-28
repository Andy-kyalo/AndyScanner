"""
provider_factory.py

Creates market data providers.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.providers.base_provider import BaseProvider
from backend.providers.csv_provider import CSVProvider
from backend.providers.mt5_provider import MT5Provider
from backend.api_provider import APIProvider


class ProviderFactory:
    """
    Factory responsible for creating market data providers.
    """

    _PROVIDERS: dict[str, type[BaseProvider]] = {
        "CSV": CSVProvider,
        "MT5": MT5Provider,
        "API": APIProvider,
    }

    @classmethod
    def create(cls, config) -> BaseProvider:
        """
        Create a provider from the scanner configuration.
        """

        provider_name = config.data_source.upper()

        provider_class = cls._PROVIDERS.get(provider_name)

        if provider_class is None:
            supported = ", ".join(sorted(cls._PROVIDERS.keys()))

            raise ValueError(
                f"Unsupported data source '{provider_name}'. "
                f"Supported providers: {supported}"
            )

        return provider_class(config)

    @classmethod
    def register(
        cls,
        name: str,
        provider: type[BaseProvider],
    ) -> None:
        """
        Register a new provider.
        """

        cls._PROVIDERS[name.upper()] = provider

    @classmethod
    def unregister(cls, name: str) -> None:
        """
        Remove a registered provider.
        """

        cls._PROVIDERS.pop(name.upper(), None)

    @classmethod
    def available_providers(cls) -> list[str]:
        """
        Return all registered providers.
        """

        return sorted(cls._PROVIDERS.keys())