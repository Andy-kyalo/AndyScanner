"""
scanner_manager.py

Central Scanner Manager.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.scanner.scanner_events import ScannerEvents
from backend.scanner.scanner_session import ScannerSession


class ScannerManager:
    """
    Coordinates scanner execution.
    """

    def __init__(self, engine=None):

        self.engine = engine

        self.session = ScannerSession()

        self.events = ScannerEvents()

    # ==================================================
    # Engine
    # ==================================================

    def attach_engine(self, engine):

        self.engine = engine

    # ==================================================
    # Execute Scan
    # ==================================================

    def run(
        self,
        market,
        timeframe,
    ):

        if self.engine is None:

            raise RuntimeError(
                "ScannerEngine is not attached."
            )

        self.session.start(
            market,
            timeframe,
        )

        self.events.dispatch(
            "scanner_started",
            session=self.session,
        )

        try:

            result = self.engine.execute_pipeline(
                market,
                timeframe,
            )

            self.session.finish()

            self.events.dispatch(
                "scanner_finished",
                session=self.session,
            )

            return result

        except Exception as error:

            self.session.fail()

            self.events.dispatch(
                "scanner_failed",
                session=self.session,
                error=error,
            )

            raise

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):

        self.session.reset()

        self.events.dispatch(
            "scanner_reset",
            session=self.session,
        )

    # ==================================================
    # Information
    # ==================================================

    @property
    def context(self):

        return self.session.context

    @property
    def state(self):

        return self.session.context.state

    def summary(self):

        return self.session.summary()