"""
performance_metrics.py

Andy Scanner
Version 5.5
"""

from datetime import datetime


class PerformanceMetrics:

    def __init__(self):

        self.started_at = datetime.now()

        self.total_scans = 0
        self.total_candles = 0

        self.total_execution_time = 0.0
        self.last_execution_time = 0.0

    def register_scan(
        self,
        execution_time,
        candles_processed,
    ):

        self.total_scans += 1

        self.total_candles += candles_processed

        self.last_execution_time = execution_time

        self.total_execution_time += execution_time

    @property
    def average_execution_time(self):

        if self.total_scans == 0:
            return 0.0

        return (
            self.total_execution_time
            / self.total_scans
        )

    @property
    def scans_per_hour(self):

        elapsed = (
            datetime.now() - self.started_at
        ).total_seconds()

        if elapsed <= 0:
            return 0.0

        return (
            self.total_scans
            / elapsed
        ) * 3600

    def summary(self):

        return {

            "started_at":
                self.started_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "total_scans":
                self.total_scans,

            "total_candles":
                self.total_candles,

            "last_execution_time":
                f"{self.last_execution_time:.3f} sec",

            "average_execution_time":
                f"{self.average_execution_time:.3f} sec",

            "scans_per_hour":
                round(
                    self.scans_per_hour,
                    2,
                ),
        }