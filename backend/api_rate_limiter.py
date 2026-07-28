"""
api_rate_limiter.py

API Rate Limiter.

Prevents excessive API requests.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import time


class APIRateLimiter:
    """
    Simple request rate limiter.
    """

    def __init__(self, requests_per_second=5):
        self.delay = 1.0 / requests_per_second
        self.last_request = 0.0

    # ==================================================
    # Wait
    # ==================================================

    def wait(self):
        """
        Wait before sending the next request.
        """

        elapsed = time.perf_counter() - self.last_request

        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

        self.last_request = time.perf_counter()

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):
        """
        Reset limiter state.
        """

        self.last_request = 0.0