"""
register_providers.py

Registers all available market data providers.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""

from backend.provider_service import get_provider_manager

from backend.providers.csv_provider import CSVProvider
from backend.providers.api_provider import APIProvider
from backend.providers.mt5_provider import MT5Provider


def register_providers():
    """
    Register all available providers using the
    shared ProviderManager instance.
    """

    manager = get_provider_manager()

    # Prevent duplicate registration
    if not manager.provider_exists("CSV"):
        manager.register("CSV", CSVProvider)

    if not manager.provider_exists("API"):
        manager.register("API", APIProvider)

    if not manager.provider_exists("MT5"):
        manager.register("MT5", MT5Provider)

    return manager