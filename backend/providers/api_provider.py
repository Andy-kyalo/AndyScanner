"""
api_provider.py

API Market Data Provider.

Concrete API provider used by Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.api_provider import APIProvider as BaseAPIProvider


class APIProvider(BaseAPIProvider):
    """
    Concrete API provider.

    Uses the shared API infrastructure from
    backend.api_provider.APIProvider.
    """

    def __init__(self, config):
        super().__init__(config)

    # ==================================================
    # Load
    # ==================================================

    def load(self, symbol=None):
        """
        Load market data through the configured API
        and convert it into Candle objects.

        Args:
            symbol:
                Provider-specific market symbol.
                If omitted, the configured canonical symbol
                is used by the base provider.
        """

        return super().load(
            symbol=symbol
        )