"""
market_manager.py

Discovers and manages available market data files.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from pathlib import Path

from config.config import Config


class MarketManager:
    """
    Handles discovery and retrieval of market data files.
    """

    def __init__(self):
        """
        Initialize the market manager.
        """
        self.data_directory = Path(Config.DATA_DIRECTORY)

    # ==========================================================
    # Validation
    # ==========================================================

    def data_directory_exists(self) -> bool:
        """
        Check whether the data directory exists.
        """
        return self.data_directory.exists()

    # ==========================================================
    # Market Discovery
    # ==========================================================

    def available_markets(self) -> list[Path]:
        """
        Return all available market CSV files.
        """

        if not self.data_directory_exists():
            return []

        return sorted(self.data_directory.glob("*.csv"))

    def market_names(self) -> list[str]:
        """
        Return all available market names.
        """

        return sorted(
            file.stem.upper()
            for file in self.available_markets()
        )

    # ==========================================================
    # Market Lookup
    # ==========================================================

    def market_path(self, market: str) -> Path | None:
        """
        Return the full path of a market CSV file.

        Example:
            US30 -> data/us30.csv
        """

        file_path = self.data_directory / f"{market.lower()}.csv"

        if file_path.exists():
            return file_path

        return None