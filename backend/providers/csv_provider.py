"""
csv_provider.py

CSV Market Data Provider.

Loads candle data from CSV files.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.loader import Loader
from backend.market_manager import MarketManager
from backend.providers.base_provider import BaseProvider


class CSVProvider(BaseProvider):
    """
    Market data provider that loads candles
    from CSV files.
    """

    def __init__(self, config):
        super().__init__(config)

        self.market_manager = MarketManager()

    # ==================================================
    # Load Market Data
    # ==================================================

    def load(self, symbol=None):
        """
        Load candle data from the configured market CSV.

        Returns
        -------
        list[Candle]
        """

        market_path = self.market_manager.market_path(
            self.config.market
        )

        if market_path is None:
            raise FileNotFoundError(
                f"Market '{self.config.market}' "
                "does not exist."
            )

        loader = Loader(str(market_path))

        return loader.load()
    # ==================================================
    # Provider Probe
    # ==================================================

    def probe(self):
        """
        Check whether the configured market CSV exists.
        """

        return (
            self.market_manager.market_path(
                self.config.market
            )
            is not None
        )
