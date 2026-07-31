"""
scanner_session.py

Scanner execution session.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime

from backend.scanner.scanner_context import ScannerContext


class ScannerSession:
    """
    Represents one complete scanner session.
    """

    def __init__(self):

        self.context = ScannerContext()

        self.session_id = None

        self.created_at = datetime.now()

    # ==================================================
    # Start Session
    # ==================================================

    def start(
        self,
        market,
        timeframe,
    ):

        self.created_at = datetime.now()

        self.session_id = self.created_at.strftime(
            "%Y%m%d%H%M%S"
        )

        self.context.start(
            market,
            timeframe,
        )

    # ==================================================
    # Finish Session
    # ==================================================

    def finish(self):

        self.context.finish()

    # ==================================================
    # Fail Session
    # ==================================================

    def fail(self):

        self.context.fail()

    # ==================================================
    # Reset Session
    # ==================================================

    def reset(self):

        self.context.reset()

        self.session_id = None

        self.created_at = datetime.now()

    # ==================================================
    # Session Metrics
    # ==================================================

    @property
    def duration(self):

        if self.context.started_at is None:
            return 0.0

        end_time = self.context.finished_at or datetime.now()

        return round(
            (end_time - self.context.started_at).total_seconds(),
            3,
        )

    @property
    def is_running(self):

        return self.context.running

    @property
    def is_finished(self):

        return self.context.finished

    @property
    def has_failed(self):

        return self.context.failed

    # ==================================================
    # Information
    # ==================================================

    def summary(self):

        return {

            "session_id": self.session_id,

            "market": self.context.market,

            "timeframe": self.context.timeframe,

            "state": self.context.state.value,

            "started_at": self.context.started_at,

            "finished_at": self.context.finished_at,

            "duration": self.duration,

            "running": self.is_running,

            "finished": self.is_finished,

            "failed": self.has_failed,

            "metadata": dict(
                self.context.metadata
            ),
        }