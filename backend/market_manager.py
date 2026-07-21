"""
market_manager.py

Discovers available market data files.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from pathlib import Path

from config.config import Config


class MarketManager:
    """
    Handles discovery of available market files.
    """

    def __init__(self):
        self.data_directory = Path(Config.DATA_DIRECTORY)

    def available_markets(self):
        """
        Returns all CSV files inside the data directory.
        """

        return sorted(self.data_directory.glob("*.csv"))

    def market_names(self):
        """
        Returns market names without .csv extension.
        """

        return [
            file.stem.upper()
            for file in self.available_markets()
        ]