"""
market_registry.py

Market Registry for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.market_manager import MarketManager


class MarketRegistry:
    """
    Registers and manages all available markets.
    """

    def __init__(self):
        self.manager = MarketManager()
        self._markets = {}

        self.refresh()

    # ==================================================
    # Refresh Registry
    # ==================================================

    def refresh(self):
        """
        Reload all available markets.
        """

        self._markets.clear()

        for name in self.manager.market_names():
            self._markets[name] = self.manager.market_path(name)

    # ==================================================
    # Get Market
    # ==================================================

    def get(self, market: str):
        """
        Return market path.
        """

        return self._markets.get(market.upper())

    # ==================================================
    # Exists
    # ==================================================

    def exists(self, market: str) -> bool:
        """
        Check whether a market exists.
        """

        return market.upper() in self._markets

    # ==================================================
    # List Markets
    # ==================================================

    def markets(self):
        """
        Return all registered market names.
        """

        return sorted(self._markets.keys())

    # ==================================================
    # Count
    # ==================================================

    def count(self):
        """
        Number of registered markets.
        """

        return len(self._markets)

    # ==================================================
    # Empty
    # ==================================================

    def is_empty(self):
        """
        True if no markets are registered.
        """

        return self.count() == 0