"""
provider_metrics.py

Provider Metrics.

Collects runtime statistics for market data providers.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from __future__ import annotations

import time


class ProviderMetrics:
    """
    Tracks runtime statistics for market data providers.

    This class records:
    - Total provider requests
    - Successful requests
    - Failed requests
    - Execution time
    - Success rate
    """

    def __init__(self):

        self._requests = 0
        self._successes = 0
        self._failures = 0
        self._total_time = 0.0

    # ==================================================
    # Manual Recording
    # ==================================================

    def record_success(self) -> None:
        """Record a successful provider request."""

        self._requests += 1
        self._successes += 1

    def record_failure(self) -> None:
        """Record a failed provider request."""

        self._requests += 1
        self._failures += 1

    # ==================================================
    # Timed Recording
    # ==================================================

    def record(self, elapsed: float, success: bool) -> None:
        """
        Record execution statistics.
        """

        self._requests += 1
        self._total_time += elapsed

        if success:
            self._successes += 1
        else:
            self._failures += 1

    # ==================================================
    # Execute & Measure
    # ==================================================

    def measure(self, function, *args, **kwargs):
        """
        Execute a callable while measuring execution time.
        """

        start = time.perf_counter()

        try:

            result = function(*args, **kwargs)

            self.record(
                time.perf_counter() - start,
                True,
            )

            return result

        except Exception:

            self.record(
                time.perf_counter() - start,
                False,
            )

            raise

    # ==================================================
    # Properties
    # ==================================================

    @property
    def requests(self) -> int:
        return self._requests

    @property
    def successes(self) -> int:
        return self._successes

    @property
    def failures(self) -> int:
        return self._failures

    @property
    def average_time(self) -> float:

        if self._requests == 0:
            return 0.0

        return self._total_time / self._requests

    @property
    def success_rate(self) -> float:

        if self._requests == 0:
            return 0.0

        return round(
            (self._successes / self._requests) * 100,
            2,
        )

    # ==================================================
    # Utilities
    # ==================================================

    def reset(self) -> None:
        """
        Reset all collected metrics.
        """

        self._requests = 0
        self._successes = 0
        self._failures = 0
        self._total_time = 0.0

    # ==================================================
    # Report
    # ==================================================

    def report(self) -> dict:
        """
        Return provider statistics.
        """

        return {
            "total_requests": self.requests,
            "successful_requests": self.successes,
            "failed_requests": self.failures,
            "success_rate": self.success_rate,
            "average_time": round(
                self.average_time,
                6,
            ),
        }