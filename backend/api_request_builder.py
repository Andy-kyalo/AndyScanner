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

    # ==================================================
    # Timeframe Mapping
    # ==================================================

    TIMEFRAME_MAP = {
        "M1": "1min",
        "M5": "5min",
        "M15": "15min",
        "M30": "30min",
        "H1": "1h",
        "H4": "4h",
        "D1": "1day",
        "W1": "1week",
        "MN1": "1month",
    }

    # ==================================================
    # Build
    # ==================================================

    @classmethod
    def build(
        cls,
        symbol,
        timeframe,
        limit=100,
        api_key=None,
    ):
        """
        Build request parameters.

        The returned parameters follow the conventions
        required by the configured REST market-data API.

        Args:
            symbol:
                Provider-specific market symbol.

            timeframe:
                AndyScanner timeframe, e.g. M5, H1.

            limit:
                Number of candles requested.

            api_key:
                API authentication key.
        """

        if not symbol:
            raise ValueError(
                "Symbol cannot be empty."
            )

        if not timeframe:
            raise ValueError(
                "Timeframe cannot be empty."
            )

        if limit <= 0:
            raise ValueError(
                "Limit must be greater than zero."
            )

        timeframe = timeframe.upper()

        interval = cls.TIMEFRAME_MAP.get(
            timeframe
        )

        if interval is None:
            raise ValueError(
                f"Unsupported timeframe: {timeframe}"
            )

        params = {
            "symbol": symbol.upper(),
            "interval": interval,
            "outputsize": limit,
        }

        if api_key:
            params["apikey"] = api_key

        return params

    # ==================================================
    # Headers
    # ==================================================

    @staticmethod
    def headers(api_key=None):
        """
        Build HTTP headers.

        Authentication is intentionally not placed
        in Authorization here because Twelve Data
        expects the API key as an `apikey` request
        parameter.
        """

        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }