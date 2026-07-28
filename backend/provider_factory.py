"""
provider_factory.py

Creates the appropriate market data provider.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.providers.csv_provider import CSVProvider
from backend.providers.base_provider import BaseProvider


class ProviderFactory:
    """
    Factory responsible for creating market data providers.
    """

    _PROVIDERS = {
        "CSV": CSVProvider,
    }

    @classmethod
    def create(cls, config) -> BaseProvider:
        """
        Create a provider based on scanner configuration.
        """

        provider_name = config.data_source.upper()

        provider_class = cls._PROVIDERS.get(provider_name)

        if provider_class is None:
            supported = ", ".join(sorted(cls._PROVIDERS))

            raise ValueError(
                f"Unsupported data source '{config.data_source}'. "
                f"Supported providers: {supported}"
            )

        return provider_class(config)

    @classmethod
    def register(cls, name: str, provider: type[BaseProvider]) -> None:
        """
        Register a new provider.
        """

        cls._PROVIDERS[name.upper()] = provider

    @classmethod
    def available_providers(cls) -> list[str]:
        """
        Return all registered providers.
        """

        return sorted(cls._PROVIDERS.keys())