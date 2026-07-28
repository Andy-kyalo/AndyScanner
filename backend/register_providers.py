"""
register_providers.py

Registers all available market data providers.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.provider_manager import ProviderManager

from backend.providers.csv_provider import CSVProvider
from backend.providers.api_provider import APIProvider
from backend.providers.mt5_provider import MT5Provider


def register_providers() -> ProviderManager:
    """
    Register every available provider.
    """

    manager = ProviderManager()

    manager.register("CSV", CSVProvider)
    manager.register("API", APIProvider)
    manager.register("MT5", MT5Provider)

    return manager