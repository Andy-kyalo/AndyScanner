"""
base_provider.py

Abstract base class for all market data providers.

Every provider must implement the load() method and
return a list of Candle objects.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """
    Base class for every market data provider.
    """

    def __init__(self, config):
        """
        Store the scanner configuration.
        """
        self.config = config

    # ==================================================
    # Load Market Data
    # ==================================================

    @abstractmethod
    def load(self):
        """
        Load market data.

        Returns:
            list[Candle]
        """
        raise NotImplementedError(
            "Every provider must implement load()."
        )

    # ==================================================
    # Provider Name
    # ==================================================

    @property
    def name(self):
        """
        Return the provider name.
        """
        return self.__class__.__name__

    # ==================================================
    # Provider Information
    # ==================================================

    def info(self):
        """
        Return provider information.
        """
        return {
            "provider": self.name,
            "market": self.config.market,
            "timeframe": self.config.timeframe,
        }