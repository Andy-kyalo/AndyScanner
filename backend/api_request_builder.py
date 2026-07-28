"""
api_request_builder.py

API Request Builder.

Builds standardized API requests.

Author: Andrew Kyalo
Project: Andy Scanner
"""


class APIRequestBuilder:
    """
    Builds request parameters.
    """

    @staticmethod
    def build(symbol, timeframe, limit=100):
        """
        Build request parameters.
        """

        return {
            "symbol": symbol,
            "timeframe": timeframe,
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