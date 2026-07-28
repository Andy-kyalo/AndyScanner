"""
api_provider.py

API market data provider.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.data_provider import DataProvider


class APIProvider(DataProvider):
    """
    Loads market data from an external API.

    This provider is a placeholder for future
    broker/API integrations.
    """

    def __init__(self, api_url=None, api_key=None):
        self.api_url = api_url
        self.api_key = api_key

    def load(self):
        """
        Load candles from an API.

        Returns
        -------
        list
            List of Candle objects.

        Raises
        ------
        NotImplementedError
            API integration has not yet been implemented.
        """

        raise NotImplementedError(
            "APIProvider is not yet implemented."
        )