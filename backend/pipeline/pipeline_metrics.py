"""
pipeline_metrics.py

Pipeline Performance Metrics.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime


class PipelineMetrics:
    """
    Collects and reports execution metrics
    for the scanner pipeline.
    """

    def __init__(self):

        self.reset()

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):

        self.total_runs = 0

        self.successful_runs = 0

        self.failed_runs = 0

        self.total_execution_time = 0.0

        self.fastest_run = None

        self.slowest_run = None

        self.last_execution = None

    # ==================================================
    # Record Execution
    # ==================================================

    def record(
        self,
        duration,
        success=True,
    ):

        duration = float(duration)

        self.total_runs += 1

        self.total_execution_time += duration

        self.last_execution = datetime.now()

        if success:

            self.successful_runs += 1

        else:

            self.failed_runs += 1

        if (
            self.fastest_run is None
            or duration < self.fastest_run
        ):

            self.fastest_run = duration

        if (
            self.slowest_run is None
            or duration > self.slowest_run
        ):

            self.slowest_run = duration

    # ==================================================
    # Statistics
    # ==================================================

    @property
    def average_execution_time(self):

        if self.total_runs == 0:

            return 0.0

        return round(

            self.total_execution_time
            / self.total_runs,

            3,

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

    @property
    def failure_rate(self):

        if self.total_runs == 0:

            return 0.0

        return round(

            (
                self.failed_runs
                / self.total_runs
            ) * 100,

            2,

        )

    # ==================================================
    # Summary
    # ==================================================

    def summary(self):

        return {

            "total_runs": self.total_runs,

            "successful_runs": self.successful_runs,

            "failed_runs": self.failed_runs,

            "success_rate": self.success_rate,

            "failure_rate": self.failure_rate,

            "average_execution_time":
                self.average_execution_time,

            "fastest_run": self.fastest_run,

            "slowest_run": self.slowest_run,

            "last_execution": self.last_execution,

        }

    # ==================================================
    # Representation
    # ==================================================

    def __repr__(self):

        return (

            f"PipelineMetrics("

            f"runs={self.total_runs}, "

            f"success_rate={self.success_rate}%)"

        )