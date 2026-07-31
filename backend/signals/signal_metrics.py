"""
signal_metrics.py

Signal Metrics.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime


class SignalMetrics:
    """
    Collects statistics for the Signal subsystem.
    """

    def __init__(self):

        self.started_at = datetime.now()

        self.generated = 0

        self.queued = 0

        self.dispatched = 0

        self.failed = 0

        self.cancelled = 0

        self.expired = 0

        self.last_signal = None

    # ==================================================
    # Counters
    # ==================================================

    def signal_generated(self):

        self.generated += 1

        self.last_signal = datetime.now()

    def signal_queued(self):

        self.queued += 1

    def signal_dispatched(self):

        self.dispatched += 1

    def signal_failed(self):

        self.failed += 1

    def signal_cancelled(self):

        self.cancelled += 1

    def signal_expired(self):

        self.expired += 1

    # ==================================================
    # Statistics
    # ==================================================

    @property
    def success_rate(self):

        total = self.dispatched + self.failed

        if total == 0:

            return 0.0

        return round(

            (self.dispatched / total) * 100,

            2,

        )

    @property
    def uptime(self):

        return round(

            (
                datetime.now()
                - self.started_at
            ).total_seconds(),

            2,

        )

    # ==================================================
    # Export
    # ==================================================

    def summary(self):

        return {

            "generated": self.generated,

            "queued": self.queued,

            "dispatched": self.dispatched,

            "failed": self.failed,

            "cancelled": self.cancelled,

            "expired": self.expired,

            "success_rate": self.success_rate,

            "uptime": self.uptime,

            "last_signal": self.last_signal,

        }

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):

        self.__init__()