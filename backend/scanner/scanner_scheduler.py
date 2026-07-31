"""
scanner_scheduler.py

Scanner Scheduler.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import threading
import time
from datetime import datetime


class ScannerScheduler:
    """
    Controls automatic scanner execution.
    """

    def __init__(self):

        self.interval = 60

        self.running = False

        self.thread = None

        self.task = None

        self.lock = threading.Lock()

        self.started_at = None

        self.stopped_at = None

        self.last_run = None

        self.total_runs = 0

        self.failed_runs = 0

    # ==================================================
    # Configuration
    # ==================================================

    def set_interval(
        self,
        seconds,
    ):

        self.interval = max(
            1,
            int(seconds),
        )

    def set_task(
        self,
        task,
    ):

        self.task = task

    # ==================================================
    # Scheduler Loop
    # ==================================================

    def _loop(self):

        while self.running:

            started = time.perf_counter()

            try:

                if self.task is not None:

                    self.task()

                self.total_runs += 1

                self.last_run = datetime.now()

            except Exception:

                self.failed_runs += 1

            elapsed = time.perf_counter() - started

            remaining = max(
                0,
                self.interval - elapsed,
            )

            time.sleep(remaining)

    # ==================================================
    # Control
    # ==================================================

    def start(self):

        with self.lock:

            if self.running:

                return

            self.running = True

            self.started_at = datetime.now()

            self.thread = threading.Thread(
                target=self._loop,
                daemon=True,
                name="ScannerScheduler",
            )

            self.thread.start()

    def stop(self):

        with self.lock:

            if not self.running:

                return

            self.running = False

            self.stopped_at = datetime.now()

        if self.thread is not None:

            self.thread.join(timeout=2)

    def restart(self):

        self.stop()

        self.start()

    # ==================================================
    # Statistics
    # ==================================================

    @property
    def active(self):

        return self.running

    @property
    def success_runs(self):

        return self.total_runs - self.failed_runs

    @property
    def success_rate(self):

        if self.total_runs == 0:

            return 0.0

        return round(
            (self.success_runs / self.total_runs) * 100,
            2,
        )

    # ==================================================
    # Summary
    # ==================================================

    def summary(self):

        return {

            "running": self.running,

            "interval": self.interval,

            "started_at": self.started_at,

            "stopped_at": self.stopped_at,

            "last_run": self.last_run,

            "total_runs": self.total_runs,

            "successful_runs": self.success_runs,

            "failed_runs": self.failed_runs,

            "success_rate": self.success_rate,
        }