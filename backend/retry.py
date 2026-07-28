"""
retry.py

Retry Manager for Andy Scanner.

Automatically retries failed operations before
raising an exception.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import time


class RetryManager:
    """
    Executes an operation with retry support.
    """

    def __init__(
        self,
        retries: int = 3,
        delay: float = 1.0,
    ):

        self.retries = retries
        self.delay = delay

    # ==========================================
    # Execute Operation
    # ==========================================

    def execute(self, operation, *args, **kwargs):
        """
        Execute a callable with retries.
        """

        last_error = None

        for attempt in range(1, self.retries + 1):

            try:
                return operation(*args, **kwargs)

            except Exception as error:

                last_error = error

                if attempt < self.retries:
                    time.sleep(self.delay)

        raise last_error

    # ==========================================
    # Update Settings
    # ==========================================

    def set_retries(self, retries: int):

        self.retries = retries

    def set_delay(self, delay: float):

        self.delay = delay