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
from backend.providers.twelvedata_provider import TwelveDataProvider


def register_providers():
    """
    Register all available market data providers.
    """

    manager = get_provider_manager()

    if not manager.provider_exists("CSV"):
        manager.register("CSV", CSVProvider)

    if not manager.provider_exists("API"):
        manager.register("API", APIProvider)

    if not manager.provider_exists("MT5"):
        manager.register("MT5", MT5Provider)

    if not manager.provider_exists("TWELVEDATA"):
        manager.register(
            "TWELVEDATA",
            TwelveDataProvider,
        )

    return manager
