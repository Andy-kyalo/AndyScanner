"""
provider_timeout.py

Provider timeout execution.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import threading

from backend.provider_exceptions import (
    ProviderTimeoutError,
)


class ProviderTimeout:
    """
    Executes a provider operation with
    a configurable timeout.
    """

    def __init__(self, timeout: float = 10.0):

        self.timeout = timeout

    # ==================================================
    # Execute
    # ==================================================

    def execute(self, operation):

        result = {}
        error = {}

        def worker():

            try:
                result["value"] = operation()

            except Exception as exc:
                error["exception"] = exc

        thread = threading.Thread(
            target=worker,
            daemon=True,
        )

        thread.start()

        thread.join(self.timeout)

        if thread.is_alive():

            raise ProviderTimeoutError(
                f"Provider operation exceeded "
                f"{self.timeout} seconds."
            )

        if "exception" in error:
            raise error["exception"]

        return result.get("value")