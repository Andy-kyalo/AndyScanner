"""
scanner_job.py

Scanner Job.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime, timedelta
import uuid


class ScannerJob:
    """
    Represents a scheduled scanner job.
    """

    def __init__(
        self,
        market,
        timeframe,
        interval=60,
        priority=1,
        enabled=True,
    ):

        self.job_id = str(uuid.uuid4())

        self.market = market.upper()

        self.timeframe = timeframe.upper()

        self.interval = max(
            1,
            int(interval),
        )

        self.priority = priority

        self.enabled = enabled

        self.created_at = datetime.now()

        self.last_run = None

        self.next_run = self.created_at

        self.total_runs = 0

        self.successful_runs = 0

        self.failed_runs = 0

    # ==================================================
    # Execution
    # ==================================================

    def mark_success(self):

        self.last_run = datetime.now()

        self.next_run = (
            self.last_run
            + timedelta(seconds=self.interval)
        )

        self.total_runs += 1

        self.successful_runs += 1

    def mark_failure(self):

        self.last_run = datetime.now()

        self.next_run = (
            self.last_run
            + timedelta(seconds=self.interval)
        )

        self.total_runs += 1

        self.failed_runs += 1

    # ==================================================
    # State
    # ==================================================

    def enable(self):

        self.enabled = True

    def disable(self):

        self.enabled = False

    @property
    def ready(self):

        return (
            self.enabled
            and datetime.now() >= self.next_run
        )

    @property
    def success_rate(self):

        if self.total_runs == 0:

            return 0.0

        return round(
            (
                self.successful_runs
                / self.total_runs
            ) * 100,
            2,
        )

    # ==================================================
    # Information
    # ==================================================

    def summary(self):

        return {

            "job_id": self.job_id,

            "market": self.market,

            "timeframe": self.timeframe,

            "interval": self.interval,

            "priority": self.priority,

            "enabled": self.enabled,

            "created_at": self.created_at,

            "last_run": self.last_run,

            "next_run": self.next_run,

            "total_runs": self.total_runs,

            "successful_runs": self.successful_runs,

            "failed_runs": self.failed_runs,

            "success_rate": self.success_rate,
        }