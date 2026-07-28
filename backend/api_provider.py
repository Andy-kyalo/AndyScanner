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


class APIProvider(BaseProvider):
    """
    Base implementation for REST API providers.

    Concrete broker providers should inherit from this class.
    """

    def __init__(self, config):
        super().__init__(config)

        self.session = APISession()
        self.cache = APICache(ttl=60)
        self.retry = APIRetryHandler()
        self.rate_limiter = APIRateLimiter()
        self.pool = APIConnectionPool()

    # ==================================================
    # Request
    # ==================================================

    def request(self, url, api_key=None, limit=100):
        """
        Execute an API request.
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

            self.cache.put(cache_key, data)

            return data

        finally:
            self.pool.release(session)

    # ==================================================
    # Load
    # ==================================================

    def load(self):
        """
        Must be implemented by concrete providers.
        """

        raise NotImplementedError(
            "API providers must implement load()."
        )