"""
api_provider.py

API Market Data Provider.

Provides market data from REST APIs.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.providers.base_provider import BaseProvider

from backend.api_session import APISession
from backend.api_cache import APICache
from backend.api_retry_handler import APIRetryHandler
from backend.api_rate_limiter import APIRateLimiter
from backend.api_request_builder import APIRequestBuilder
from backend.api_response_handler import APIResponseHandler
from backend.api_connection_pool import APIConnectionPool

from backend.mapping.json_mapper import JSONMapper


class APIProvider(BaseProvider):
    """
    Base implementation for REST API providers.

    Concrete API providers can inherit from this class.
    """

    def __init__(self, config):

        super().__init__(config)

        self.session = APISession()
        self.cache = APICache(ttl=60)
        self.retry = APIRetryHandler()
        self.rate_limiter = APIRateLimiter()
        self.pool = APIConnectionPool()

        self.mapper = JSONMapper()

    # ==================================================
    # Request
    # ==================================================

    def request(
        self,
        url,
        symbol=None,
        api_key=None,
        limit=100,
    ):
        """
        Execute an API request and return
        the raw JSON response.
        """

        request_symbol = (
            symbol
            or self.config.market
        )

        cache_key = (
            request_symbol,
            self.config.timeframe,
            limit,
        )

        cached = self.cache.get(cache_key)

        if cached is not None:
            return cached

        headers = APIRequestBuilder.headers(api_key)

        params = APIRequestBuilder.build(
            request_symbol,
            self.config.timeframe,
            limit,
            api_key=api_key
        )

        self.session.set_headers(headers)

        self.rate_limiter.wait()

        session = self.pool.acquire()

        try:

            response = self.retry.execute(
                session.get,
                url,
                params=params,
                timeout=15,
            )

            data = APIResponseHandler.parse(response)

            self.cache.put(
                cache_key,
                data,
            )

            return data

        finally:

            self.pool.release(session)

    # ==================================================
    # Map JSON
    # ==================================================

    def map_candles(self, raw_data):
        """
        Convert raw JSON market data
        into Candle objects.
        """

        return self.mapper.map(raw_data)

    # ==================================================
    # Provider Probe
    # ==================================================

    def probe(self):
        """
        Perform a lightweight API provider readiness check.

        This does not request market data.
        """

        self.probe_error = None

        api_url = getattr(
            self.config,
            "api_url",
            None,
        )

        if not api_url:
            self.probe_error = (
                "API URL is not configured."
            )
            return False

        if not callable(
            getattr(self, "request", None)
        ):
            self.probe_error = (
                "API request method is unavailable."
            )
            return False

        return True

    # ==================================================
    # Load
    # ==================================================

    def load(self, symbol=None):
        """
        Load market data from the configured API
        and convert it into Candle objects.

        Args:
            symbol:
                Provider-specific market symbol.
                If omitted, the canonical market symbol
                from the configuration is used.

        Returns:
            list[Candle]
        """

        api_url = getattr(
            self.config,
            "api_url",
            None,
        )

        api_key = getattr(
            self.config,
            "api_key",
            None,
        )

        if not api_url:
            raise ValueError(
                "API URL is not configured."
            )

        raw_response = self.request(
            url=api_url,
            symbol=symbol,
            api_key=api_key,
            limit=500,
        )

        if isinstance(raw_response, dict):

            raw_data = raw_response.get(
                "values"
            )

        else:

            raw_data = raw_response

        if raw_data is None:
            raise ValueError(
                "API response contains no market data."
            )

        return self.map_candles(raw_data)