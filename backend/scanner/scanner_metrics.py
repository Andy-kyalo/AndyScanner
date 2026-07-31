"""
scanner_metrics.py

Scanner Metrics.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime


class ScannerMetrics:
    """
    Collects scheduler and scanner performance metrics.
    """

    def __init__(self):

        self.started_at = datetime.now()

        self.total_jobs = 0

        self.completed_jobs = 0

        self.failed_jobs = 0

        self.total_cycles = 0

        self.last_cycle = None

        self.last_success = None

        self.last_failure = None

    # ==================================================
    # Cycle Metrics
    # ==================================================

    def cycle_started(self):

        self.total_cycles += 1

        self.last_cycle = datetime.now()

    # ==================================================
    # Job Metrics
    # ==================================================

    def job_registered(self):

        self.total_jobs += 1

    def job_completed(self):

        self.completed_jobs += 1

        self.last_success = datetime.now()

    def job_failed(self):

        self.failed_jobs += 1

        self.last_failure = datetime.now()

    # ==================================================
    # Derived Statistics
    # ==================================================

    @property
    def success_rate(self):

        total = self.completed_jobs + self.failed_jobs

        if total == 0:

            return 0.0

        return round(

            (self.completed_jobs / total) * 100,

            2,

        )

    @property
    def failure_rate(self):

        total = self.completed_jobs + self.failed_jobs

        if total == 0:

            return 0.0

        return round(

            (self.failed_jobs / total) * 100,

            2,

        )

    @property
    def uptime_seconds(self):

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

            "started_at": self.started_at,

            "uptime_seconds": self.uptime_seconds,

            "total_cycles": self.total_cycles,

            "registered_jobs": self.total_jobs,

            "completed_jobs": self.completed_jobs,

            "failed_jobs": self.failed_jobs,

            "success_rate": self.success_rate,

            "failure_rate": self.failure_rate,

            "last_cycle": self.last_cycle,

            "last_success": self.last_success,

            "last_failure": self.last_failure,

        }

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):

        self.__init__()