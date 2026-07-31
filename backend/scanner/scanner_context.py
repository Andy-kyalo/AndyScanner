"""
scanner_context.py

Scanner execution context.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime

from backend.scanner.scanner_state import ScannerState


class ScannerContext:
    """
    Holds the current scanner execution context.
    """

    def __init__(self):

        self.market = None
        self.timeframe = None

        self.started_at = None
        self.finished_at = None

        self.state = ScannerState.IDLE

        self.metadata = {}

    # ==================================================
    # Lifecycle
    # ==================================================

    def start(self, market, timeframe):

        self.market = market
        self.timeframe = timeframe

        self.started_at = datetime.now()
        self.finished_at = None

        self.state = ScannerState.RUNNING

    def finish(self):

        self.finished_at = datetime.now()
        self.state = ScannerState.STOPPED

    def fail(self):

        self.finished_at = datetime.now()
        self.state = ScannerState.ERROR

    def reset(self):

        self.market = None
        self.timeframe = None

        self.started_at = None
        self.finished_at = None

        self.metadata.clear()

        self.state = ScannerState.IDLE

    # ==================================================
    # Metadata
    # ==================================================

    def set(self, key, value):

        self.metadata[key] = value

    def get(self, key, default=None):

        return self.metadata.get(key, default)

    # ==================================================
    # Status
    # ==================================================

    @property
    def running(self):

        return self.state == ScannerState.RUNNING

    @property
    def finished(self):

        return self.state == ScannerState.STOPPED

    @property
    def failed(self):

        return self.state == ScannerState.ERROR