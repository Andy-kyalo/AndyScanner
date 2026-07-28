"""
mt5_provider.py

MetaTrader 5 Market Data Provider.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.providers.base_provider import BaseProvider


class MT5Provider(BaseProvider):
    """
    Loads market data from MetaTrader 5.

    This provider will be implemented later when
    live broker integration is added.
    """

    def __init__(self, config):
        super().__init__(config)

        self.connected = False

    # ==================================================
    # Connection
    # ==================================================

    def connect(self):
        """
        Connect to MT5.
        """
        raise NotImplementedError(
            "MT5 connection is not implemented yet."
        )

    def disconnect(self):
        """
        Disconnect from MT5.
        """
        self.connected = False

    def is_connected(self):
        """
        Return connection status.
        """
        return self.connected

    # ==================================================
    # Load Market Data
    # ==================================================

    def load(self):
        """
        Load candles from MT5.
        """

        raise NotImplementedError(
            "MT5Provider has not been implemented yet."
        )