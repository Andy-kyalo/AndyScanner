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

    def request(self, url, api_key=None, limit=100):
        """
        Execute an API request and return
        the raw JSON response.
        """

        cache_key = (
            self.config.market,
            self.config.timeframe,
            limit,
        )

        cached = self.cache.get(cache_key)

        if cached is not None:
            return cached

        headers = APIRequestBuilder.headers(api_key)

        params = APIRequestBuilder.build(
            self.config.market,
            self.config.timeframe,
            limit,
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
    # Load
    # ==================================================

    def load(self):
        """
        Load and map market data.

        Concrete providers should normally override
        the API URL/request details.
        """

        raise NotImplementedError(
            "APIProvider.load() requires a concrete "
            "API provider implementation."
        )