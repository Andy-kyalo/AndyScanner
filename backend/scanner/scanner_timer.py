"""
scanner_timer.py

Scanner Timer.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import threading
import time


class ScannerTimer:
    """
    Coordinates periodic execution of scanner jobs.
    """

    def __init__(
        self,
        queue,
        executor,
        interval=1,
    ):

        self.queue = queue

        self.executor = executor

        self.interval = max(
            1,
            int(interval),
        )

        self._running = False

        self._thread = None

    # ==================================================
    # Main Loop
    # ==================================================

    def _loop(self):

        while self._running:

            try:

                self.executor.execute_queue(
                    self.queue,
                )

            except Exception:

                pass

            time.sleep(self.interval)

    # ==================================================
    # Control
    # ==================================================

    def start(self):

        if self._running:

            return

        self._running = True

        self._thread = threading.Thread(
            target=self._loop,
            daemon=True,
            name="ScannerTimer",
        )

        self._thread.start()

    def stop(self):

        self._running = False

        if self._thread:

            self._thread.join(
                timeout=2,
            )

    def restart(self):

        self.stop()

        self.start()

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

    # ==================================================
    # Status
    # ==================================================

    @property
    def running(self):

        return self._running

    @property
    def alive(self):

        return (

            self._thread is not None

            and self._thread.is_alive()

        )

    def summary(self):

        return {

            "running": self.running,

            "alive": self.alive,

            "interval": self.interval,

        }