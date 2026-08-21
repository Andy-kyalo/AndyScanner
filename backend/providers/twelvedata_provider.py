"""
twelvedata_provider.py

Twelve Data live market-data provider.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.providers.base_provider import BaseProvider
from backend.candle import Candle
from backend.symbol_mapping.symbol_resolver import SymbolResolver

import requests


class TwelveDataProvider(BaseProvider):
    """
    Market-data provider using Twelve Data REST API.
    """

    BASE_URL = "https://api.twelvedata.com/time_series"

    TIMEFRAME_MAP = {
        "M1": "1min",
        "M5": "5min",
        "M15": "15min",
        "M30": "30min",
        "H1": "1h",
        "H4": "4h",
        "D1": "1day",
    }

    def __init__(self, config):
        super().__init__(config)

        self.api_key = getattr(
            config,
            "api_key",
            None,
        )

        self.api_url = (
            getattr(config, "api_url", None)
            or self.BASE_URL
        )

        self.timeout = 15

    # ==================================================
    # Timeframe
    # ==================================================

    def _interval(self):
        timeframe = self.config.timeframe.upper()

        try:
            return self.TIMEFRAME_MAP[timeframe]
        except KeyError:
            raise ValueError(
                f"Unsupported Twelve Data timeframe: "
                f"{timeframe}"
            )

            # ==================================================
    # Provider Probe
    # ==================================================

    def probe(self):
        """
        Perform a lightweight Twelve Data readiness check.

        No market-data request is made.
        """

        self.probe_error = None

        if not self.api_key:
            self.probe_error = (
                "Twelve Data API key is not configured."
            )
            return False

        resolution = SymbolResolver.resolve(
            self.config.market,
            "TWELVEDATA",
        )

        if not resolution.supported:
            self.probe_error = (
                f"Market '{resolution.canonical}' "
                "is not supported by Twelve Data."
            )
            return False

        return True

    # ==================================================
    # Request
    # ==================================================

    def request(self, limit=500):
        """
        Request OHLC data from Twelve Data.
        """

        if not self.api_key:
            raise RuntimeError(
                "Twelve Data API key is not configured."
            )

        resolution = SymbolResolver.resolve(
            self.config.market,
            "TWELVEDATA",
        )

        if not resolution.supported:
            raise RuntimeError(
                f"Twelve Data does not support canonical market "
                f"'{resolution.canonical}' with a configured symbol."
            )

        params = {
            "symbol": resolution.symbol,
            "interval": self._interval(),
            "outputsize": limit,
            "apikey": self.api_key,
            "format": "JSON",
            "timezone": "UTC",
        }

        response = requests.get(
            self.api_url,
            params=params,
            timeout=self.timeout,
        )

        try:
            data = response.json()
        except ValueError as error:
            raise RuntimeError(
                "Twelve Data returned invalid JSON."
            ) from error

        if response.status_code != 200:
            raise RuntimeError(
                f"Twelve Data HTTP error "
                f"{response.status_code}: {data}"
            )

        if isinstance(data, dict) and data.get("status") == "error":
            raise RuntimeError(
                f"Twelve Data API error: "
                f"{data.get('message', data)}"
            )

        return data

    # ==================================================
    # Candle Mapping
    # ==================================================

    def map_candles(self, response):
        """
        Convert Twelve Data time-series response
        into Andy Scanner Candle objects.
        """

        values = response.get("values")

        if not values:
            raise ValueError(
                "Twelve Data response contains no candle values."
            )

        candles = []

        for item in reversed(values):

            try:
                candles.append(
                    Candle(
                        time=item["datetime"],
                        open_price=float(item["open"]),
                        high=float(item["high"]),
                        low=float(item["low"]),
                        close=float(item["close"]),
                    )
                )

            except (KeyError, TypeError, ValueError) as error:
                raise ValueError(
                    f"Invalid Twelve Data candle: "
                    f"{item}"
                ) from error

        return candles

    # ==================================================
    # Load
    # ==================================================

            # ==================================================
    # Load
    # ==================================================

    def load(self, symbol=None):
        """
        Load live/historical intraday candles.

        Args:
            symbol:
                Provider-specific Twelve Data symbol.
                If omitted, SymbolResolver resolves the
                configured canonical market.
        """

        if symbol is None:

            response = self.request(
                limit=500,
            )

        else:

            resolution = SymbolResolver.resolve(
                self.config.market,
                "TWELVEDATA",
            )

            if not resolution.supported:
                raise RuntimeError(
                    f"Twelve Data does not support canonical market "
                    f"'{self.config.market}'."
                )

            params = {
                "symbol": symbol,
                "interval": self._interval(),
                "outputsize": 500,
                "apikey": self.api_key,
                "format": "JSON",
                "timezone": "UTC",
            }

            response = requests.get(
                self.api_url,
                params=params,
                timeout=self.timeout,
            )

            try:
                data = response.json()
            except ValueError as error:
                raise RuntimeError(
                    "Twelve Data returned invalid JSON."
                ) from error

            if response.status_code != 200:
                raise RuntimeError(
                    f"Twelve Data HTTP error "
                    f"{response.status_code}: {data}"
                )

            if (
                isinstance(data, dict)
                and data.get("status") == "error"
            ):
                raise RuntimeError(
                    f"Twelve Data API error: "
                    f"{data.get('message', data)}"
                )

            response = data

        return self.map_candles(response)