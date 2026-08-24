"""
twelvedata_provider.py

Twelve Data live market-data provider.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import requests

from backend.providers.base_provider import BaseProvider
from backend.candle import Candle
from backend.symbol_mapping.symbol_resolver import SymbolResolver
from backend.provider_exceptions import (
    ProviderAuthenticationError,
    ProviderConnectionError,
    ProviderDataError,
    ProviderMarketUnsupportedError,
    ProviderPlanRestrictedError,
    ProviderRateLimitError,
    ProviderTimeoutError,
    ProviderUnavailableError,
)


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
        """
        Convert AndyScanner timeframe into
        Twelve Data interval format.
        """

        timeframe = self.config.timeframe.upper()

        try:
            return self.TIMEFRAME_MAP[timeframe]

        except KeyError as error:

            raise ValueError(
                f"Unsupported Twelve Data timeframe: "
                f"{timeframe}"
            ) from error

    # ==================================================
    # Symbol Resolution
    # ==================================================

    def _resolve_symbol(self, symbol=None):
        """
        Resolve the provider-specific symbol.

        If an explicit provider symbol is supplied,
        use it.

        Otherwise resolve the configured canonical
        AndyScanner market through SymbolResolver.
        """

        if symbol:
            return symbol

        resolution = SymbolResolver.resolve(
            self.config.market,
            "TWELVEDATA",
        )

        if not resolution.supported:

            raise ProviderMarketUnsupportedError(
                f"Market '{resolution.canonical}' "
                "is not supported by Twelve Data."
            )

        return resolution.symbol

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

        try:

            self._interval()

        except ValueError as error:

            self.probe_error = str(error)

            return False

        try:

            self._resolve_symbol()

        except ProviderMarketUnsupportedError as error:

            self.probe_error = str(error)

            return False

        return True

    # ==================================================
    # Error Classification
    # ==================================================

    def _raise_api_error(
        self,
        status_code,
        data,
    ):
        """
        Convert Twelve Data HTTP/API errors into
        structured AndyScanner provider exceptions.
        """

        if isinstance(data, dict):

            message = str(
                data.get(
                    "message",
                    data,
                )
            )

            code = data.get(
                "code",
                status_code,
            )

        else:

            message = str(data)
            code = status_code

        normalized = message.lower()

        # --------------------------------------------------
        # Authentication
        # --------------------------------------------------

        if (
            status_code in (401, 403)
            or "apikey" in normalized
            or "api key" in normalized
            or "authentication" in normalized
            or "unauthorized" in normalized
        ):

            raise ProviderAuthenticationError(
                f"Twelve Data authentication failed: "
                f"{message}"
            )

        # --------------------------------------------------
        # Rate Limit / Quota
        # --------------------------------------------------

        if (
            status_code == 429
            or "rate limit" in normalized
            or "too many requests" in normalized
            or "quota" in normalized
            or "credits" in normalized
        ):

            raise ProviderRateLimitError(
                f"Twelve Data rate limit/quota reached: "
                f"{message}"
            )

        # --------------------------------------------------
        # Plan Restriction
        # --------------------------------------------------

        if (
            "available starting with" in normalized
            or "grow or venture plan" in normalized
            or "upgrade" in normalized
            or "plan" in normalized
            and (
                "required" in normalized
                or "available" in normalized
                or "restricted" in normalized
            )
        ):

            raise ProviderPlanRestrictedError(
                f"Twelve Data plan restriction: "
                f"{message}"
            )

        # --------------------------------------------------
        # Invalid / Unsupported Symbol
        # --------------------------------------------------

        if (
            "symbol" in normalized
            and (
                "invalid" in normalized
                or "not found" in normalized
                or "missing" in normalized
                or "unsupported" in normalized
            )
        ):

            raise ProviderMarketUnsupportedError(
                f"Twelve Data market/symbol error: "
                f"{message}"
            )

        # --------------------------------------------------
        # Provider Availability
        # --------------------------------------------------

        if status_code >= 500:

            raise ProviderUnavailableError(
                f"Twelve Data server error "
                f"{status_code}: {message}"
            )

        # --------------------------------------------------
        # Generic Provider Error
        # --------------------------------------------------

        raise ProviderUnavailableError(
            f"Twelve Data API error "
            f"{code}: {message}"
        )

    # ==================================================
    # Request
    # ==================================================

    def request(
        self,
        limit=500,
        symbol=None,
    ):
        """
        Request OHLC data from Twelve Data.

        Args:
            limit:
                Number of candles requested.

            symbol:
                Optional provider-specific symbol.

        Returns:
            Raw Twelve Data response dictionary.
        """

        if not self.api_key:

            raise ProviderAuthenticationError(
                "Twelve Data API key is not configured."
            )

        if limit <= 0:

            raise ValueError(
                "Candle limit must be greater than zero."
            )

        request_symbol = self._resolve_symbol(
            symbol
        )

        params = {
            "symbol": request_symbol,
            "interval": self._interval(),
            "outputsize": limit,
            "apikey": self.api_key,
            "format": "JSON",
            "timezone": "UTC",
        }

        try:

            response = requests.get(
                self.api_url,
                params=params,
                timeout=self.timeout,
            )

        except requests.Timeout as error:

            raise ProviderTimeoutError(
                "Twelve Data request timed out."
            ) from error

        except requests.ConnectionError as error:

            raise ProviderConnectionError(
                "Unable to connect to Twelve Data."
            ) from error

        except requests.RequestException as error:

            raise ProviderConnectionError(
                f"Twelve Data request failed: {error}"
            ) from error

        # --------------------------------------------------
        # Parse JSON
        # --------------------------------------------------

        try:

            data = response.json()

        except ValueError as error:

            raise ProviderDataError(
                "Twelve Data returned invalid JSON."
            ) from error

        # --------------------------------------------------
        # HTTP Errors
        # --------------------------------------------------

        if response.status_code != 200:

            self._raise_api_error(
                response.status_code,
                data,
            )

        # --------------------------------------------------
        # API-Level Errors
        # --------------------------------------------------

        if (
            isinstance(data, dict)
            and data.get("status") == "error"
        ):

            self._raise_api_error(
                response.status_code,
                data,
            )

        return data

    # ==================================================
    # Candle Mapping
    # ==================================================

    def map_candles(self, response):
        """
        Convert Twelve Data time-series response
        into AndyScanner Candle objects.
        """

        if not isinstance(response, dict):

            raise ProviderDataError(
                "Twelve Data response must be a dictionary."
            )

        values = response.get("values")

        if not values:

            raise ProviderDataError(
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

            except (
                KeyError,
                TypeError,
                ValueError,
            ) as error:

                raise ProviderDataError(
                    f"Invalid Twelve Data candle: "
                    f"{item}"
                ) from error

        return candles

    # ==================================================
    # Load
    # ==================================================

    def load(self, symbol=None):
        """
        Load live/historical intraday candles.

        Args:
            symbol:
                Optional provider-specific Twelve Data
                symbol.

                If omitted, SymbolResolver resolves the
                configured canonical market.

        Returns:
            list[Candle]
        """

        response = self.request(
            limit=500,
            symbol=symbol,
        )

        return self.map_candles(
            response
)
