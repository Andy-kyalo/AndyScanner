"""
provider_retry.py

Retry mechanism for market data providers.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import time

from backend.provider_exceptions import (
    ProviderConnectionError,
    ProviderTimeoutError,
    ProviderUnavailableError,
)


class ProviderRetry:
    """
    Executes provider operations with configurable
    retry attempts.
    """

    RETRYABLE_ERRORS = (
        ProviderConnectionError,
        ProviderTimeoutError,
        ProviderUnavailableError,
    )

    def __init__(
        self,
        retries: int = 3,
        delay: float = 1.0,
    ):

        self.retries = max(1, retries)
        self.delay = max(0.0, delay)

    # ==================================================
    # Execute
    # ==================================================

    def execute(self, operation):

        last_exception = None

        for attempt in range(
            1,
            self.retries + 1,
        ):

            try:

                return operation()

            except self.RETRYABLE_ERRORS as error:

                last_exception = error

                if attempt < self.retries:

                    time.sleep(self.delay)

        if last_exception is not None:
            raise last_exception

        raise RuntimeError(
            "Provider retry failed without an exception."
        )