"""
api_retry_handler.py

API Retry Handler.

Automatically retries failed API requests.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import time


class APIRetryHandler:
    """
    Handles automatic retries.
    """

    def __init__(self, retries=3, delay=1):
        self.retries = retries
        self.delay = delay

    # ==================================================
    # Execute
    # ==================================================

    def execute(self, function, *args, **kwargs):
        """
        Execute a function with retry support.
        """

        last_error = None

        for attempt in range(self.retries):

            try:
                return function(*args, **kwargs)

            except Exception as error:

                last_error = error

                if attempt < self.retries - 1:
                    time.sleep(self.delay)

        raise last_error