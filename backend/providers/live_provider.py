"""
live_provider.py

Abstract base for live market providers.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from abc import ABC, abstractmethod

from backend.providers.base_provider import BaseProvider


class LiveProvider(BaseProvider, ABC):
    """
    Base class for every live market provider.
    """

    @abstractmethod
    def connect(self):
        """Connect to broker/API."""
        pass

    @abstractmethod
    def disconnect(self):
        """Disconnect from broker/API."""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Return connection status."""
        pass

    @abstractmethod
    def get_latest_candle(self):
        """Return latest candle."""
        pass

    @abstractmethod
    def get_candles(self, limit=500):
        """Return historical candles."""
        pass

    def load(self):
        """
        Required by BaseProvider.
        """
        return self.get_candles()