"""
provider_retry.py

Retry mechanism for market data providers.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import time

from backend.provider_exceptions import (
    ProviderTimeoutError,
    ProviderConnectionError,
    ProviderUnavailableError,
)


class ProviderRetry:
    """
    Executes provider operations with
    configurable retry attempts.
    """

    def __init__(
        self,
        retries: int = 3,
        delay: float = 1.0,
    ):

        self.retries = retries
        self.delay = delay

    # ==================================================
    # Execute
    # ==================================================

    def execute(self, operation):

        last_exception = None

        for attempt in range(1, self.retries + 1):

            try:

                return operation()

            except (
                ProviderConnectionError,
                ProviderTimeoutError,
                ProviderUnavailableError,
            ) as error:

                last_exception = error

                if attempt < self.retries:

                    time.sleep(self.delay)

        raise last_exception