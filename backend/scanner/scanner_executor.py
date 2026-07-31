"""
scanner_executor.py

Scanner Executor.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime


class ScannerExecutor:
    """
    Executes scheduled scanner jobs.
    """

    def __init__(
        self,
        manager,
        logger=None,
    ):

        self.manager = manager

        self.logger = logger

        self.total_executions = 0

        self.successful_executions = 0

        self.failed_executions = 0

        self.last_execution = None

    # ==================================================
    # Execute Job
    # ==================================================

    def execute(self, job):

        self.total_executions += 1

        self.last_execution = datetime.now()

        try:

            result = self.manager.run(
                job.market,
                job.timeframe,
            )

            job.mark_success()

            self.successful_executions += 1

            if self.logger:

                self.logger.info(
                    f"Job executed successfully "
                    f"[{job.market} {job.timeframe}]"
                )

            return result

        except Exception as error:

            job.mark_failure()

            self.failed_executions += 1

            if self.logger:

                self.logger.error(
                    f"Job execution failed "
                    f"[{job.market} {job.timeframe}] : {error}"
                )

            return None

    # ==================================================
    # Queue Execution
    # ==================================================

    def execute_queue(self, queue):

        results = []

        for job in queue.ready_jobs():

            result = self.execute(job)

            if result is not None:

                results.append(result)

        return results

    # ==================================================
    # Statistics
    # ==================================================

    @property
    def success_rate(self):

        if self.total_executions == 0:

            return 0.0

        return round(

            (
                self.successful_executions
                / self.total_executions
            ) * 100,

            2,

        )

    def summary(self):

        return {

            "total_executions": self.total_executions,

            "successful_executions": self.successful_executions,

            "failed_executions": self.failed_executions,

            "success_rate": self.success_rate,

            "last_execution": self.last_execution,

        }