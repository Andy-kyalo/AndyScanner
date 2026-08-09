"""
api_request_builder.py

API Request Builder.

Builds standardized API requests.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""


class APIRequestBuilder:
    """
    Builds standardized API request parameters
    and HTTP headers.
    """

    @staticmethod
    def build(symbol, timeframe, limit=100):
        """
        Build request parameters.
        """

        if not symbol:
            raise ValueError("Symbol cannot be empty.")

        if not timeframe:
            raise ValueError("Timeframe cannot be empty.")

        if limit <= 0:
            raise ValueError(
                "Limit must be greater than zero."
            )

        return {
            "symbol": symbol.upper(),
            "timeframe": timeframe.upper(),
            "limit": limit,
        }

    @staticmethod
    def headers(api_key=None):
        """
        Build request headers.
        """

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if api_key:
            headers["Authorization"] = (
                f"Bearer {api_key}"
            )

        return headers
