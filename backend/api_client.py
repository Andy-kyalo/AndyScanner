"""
api_client.py

Base API Client for Andy Scanner.

Every market data provider should inherit from this class.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from abc import ABC, abstractmethod

from backend.api_response import APIResponse


class APIClient(ABC):
    """
    Abstract base class for all API clients.
    """

    def __init__(self):

        self.connected = False

    # ==========================================
    # Connection
    # ==========================================

    @abstractmethod
    def connect(self):
        """
        Establish connection to the provider.
        """
        pass

    # ==========================================
    # Disconnect
    # ==========================================

    @abstractmethod
    def disconnect(self):
        """
        Close provider connection.
        """
        pass

    # ==========================================
    # Health Check
    # ==========================================

    @abstractmethod
    def is_connected(self):
        """
        Return connection status.
        """
        pass

    # ==========================================
    # Market Data
    # ==========================================

    @abstractmethod
    def get_candles(
        self,
        market,
        timeframe,
        limit=500,
    ):
        """
        Retrieve market candles.
        """
        pass

    # ==========================================
    # Success Response
    # ==========================================

    def success(
        self,
        message,
        data=None,
    ):

        return APIResponse(
            success=True,
            message=message,
            data=data,
        )