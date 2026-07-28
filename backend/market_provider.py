"""
market_provider.py

Abstract interface for all market data providers.

Every broker, exchange or data source must inherit
from this class and implement the required methods.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from abc import ABC, abstractmethod


class MarketProvider(ABC):
    """
    Base class for every market data provider.
    """

    def __init__(self, symbol, timeframe):

        self.symbol = symbol
        self.timeframe = timeframe

    @abstractmethod
    def connect(self):
        """
        Connect to the market source.
        """
        pass

    @abstractmethod
    def disconnect(self):
        """
        Disconnect from the market source.
        """
        pass

    @abstractmethod
    def get_latest_candle(self):
        """
        Return the latest market candle.
        """
        pass

    @abstractmethod
    def get_candles(self, limit=100):
        """
        Return historical candles.
        """
        pass

    @abstractmethod
    def is_connected(self):
        """
        Return True if connected.
        """
        pass