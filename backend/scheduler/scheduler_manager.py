"""
scheduler_manager.py

Professional Scheduler Manager

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime


class SchedulerManager:
    """
    Controls automatic scanner execution.
    """

    def __init__(self, interval=300):

        self.running = False
        self.interval = interval

        self.scan_counter = 0

        self.session_start = None
        self.last_scan = None

    # -----------------------------------------

    def start(self):

        self.running = True
        self.session_start = datetime.now()

    # -----------------------------------------

    def stop(self):

        self.running = False

    # -----------------------------------------

    def register_scan(self):

        self.scan_counter += 1
        self.last_scan = datetime.now()

    # -----------------------------------------

    def uptime(self):

        if self.session_start is None:
            return "00:00:00"

        elapsed = datetime.now() - self.session_start
        return str(elapsed).split(".")[0]

    # -----------------------------------------

    def summary(self):

        return {

            "running": self.running,

            "interval": self.interval,

            "scan_counter": self.scan_counter,

            "session_start": (
                self.session_start.strftime("%Y-%m-%d %H:%M:%S")
                if self.session_start
                else "Not Started"
            ),

            "last_scan": (
                self.last_scan.strftime("%Y-%m-%d %H:%M:%S")
                if self.last_scan
                else "None"
            ),

            "uptime": self.uptime()

        }