"""
scanner_queue.py

Scanner Job Queue.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from threading import Lock


class ScannerQueue:
    """
    Central queue for scheduled scanner jobs.
    """

    def __init__(self):

        self._jobs = []

        self._lock = Lock()

    # ==================================================
    # Registration
    # ==================================================

    def add(self, job):

        with self._lock:

            for existing in self._jobs:

                if (
                    existing.market == job.market
                    and existing.timeframe == job.timeframe
                ):
                    return False

            self._jobs.append(job)

            self._sort()

            return True

    def remove(
        self,
        market,
        timeframe,
    ):

        with self._lock:

            for job in self._jobs:

                if (
                    job.market == market
                    and job.timeframe == timeframe
                ):
                    self._jobs.remove(job)
                    return True

        return False

    def clear(self):

        with self._lock:

            self._jobs.clear()

    # ==================================================
    # Lookup
    # ==================================================

    def find(
        self,
        market,
        timeframe,
    ):

        with self._lock:

            for job in self._jobs:

                if (
                    job.market == market
                    and job.timeframe == timeframe
                ):
                    return job

        return None

    def jobs(self):

        with self._lock:

            return list(self._jobs)

    # ==================================================
    # Enable / Disable
    # ==================================================

    def enable(
        self,
        market,
        timeframe,
    ):

        job = self.find(
            market,
            timeframe,
        )

        if job:

            job.enable()

            return True

        return False

    def disable(
        self,
        market,
        timeframe,
    ):

        job = self.find(
            market,
            timeframe,
        )

        if job:

            job.disable()

            return True

        return False

    # ==================================================
    # Ready Jobs
    # ==================================================

    def ready_jobs(self):

        ready = []

        with self._lock:

            for job in self._jobs:

                if job.enabled and job.ready:

                    ready.append(job)

        return ready

    # ==================================================
    # Queue Information
    # ==================================================

    def count(self):

        return len(self._jobs)

    def active_count(self):

        return len(

            [

                job

                for job in self._jobs

                if job.enabled

            ]

        )

    def summary(self):

        return {

            "total_jobs": self.count(),

            "active_jobs": self.active_count(),

            "inactive_jobs": self.count()
            - self.active_count(),

        }

    # ==================================================
    # Internal
    # ==================================================

    def _sort(self):

        self._jobs.sort(

            key=lambda job: (

                -job.priority,

                job.market,

                job.timeframe,

            )

        )
