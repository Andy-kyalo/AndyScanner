"""
api_provider.py

API Market Data Provider.

Loads market data from external APIs.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.providers.base_provider import BaseProvider


class APIProvider(BaseProvider):
    """
    Loads market data from an external API.

    This provider is a placeholder for future
    live market integrations.
    """

    def __init__(self, config):
        super().__init__(config)

    # ==================================================
    # Load Market Data
    # ==================================================

    def load(self):
        """
        Load market data from an external API.

        Returns:
            list[Candle]
        """

        raise NotImplementedError(
            "APIProvider has not been implemented yet."
        )