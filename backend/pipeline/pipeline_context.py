"""
pipeline_context.py

Scanner Pipeline Context.

Carries data between every stage of the scanner pipeline.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime


class PipelineContext:
    """
    Shared execution context for the scanner pipeline.
    """

    def __init__(self):

        self.reset()

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):

        self.market = None
        self.timeframe = None

        self.provider = None
        self.mapper = None

        self.raw_data = None
        self.candles = None

        self.analyzer = None
        self.signal = None
        self.trade_setup = None
        
        self.scan_result = None

        self.session = None
        self.report = None

        self.database_result = None

        self.error = None

        self.metadata = {}

        self.started_at = None
        self.finished_at = None
        
        

    # ==================================================
    # Start
    # ==================================================

    def start(
        self,
        market,
        timeframe,
    ):

        self.market = market
        self.timeframe = timeframe

        self.started_at = datetime.now()

    # ==================================================
    # Finish
    # ==================================================

    def finish(self):

        self.finished_at = datetime.now()

    # ==================================================
    # Duration
    # ==================================================

    @property
    def duration(self):

        if (
            self.started_at is None
            or self.finished_at is None
        ):
            return 0.0

        return round(
            (
                self.finished_at
                - self.started_at
            ).total_seconds(),
            3,
        )

    # ==================================================
    # Error Handling
    # ==================================================

    def set_error(
        self,
        exception,
    ):

        self.error = exception

    @property
    def has_error(self):

        return self.error is not None

    # ==================================================
    # Metadata
    # ==================================================

    def set_metadata(
        self,
        key,
        value,
    ):

        self.metadata[key] = value

    def get_metadata(
        self,
        key,
        default=None,
    ):

        return self.metadata.get(
            key,
            default,
        )

    # ==================================================
    # Summary
    # ==================================================

    def summary(self):

        return {

            "market": self.market,

            "timeframe": self.timeframe,

            "provider": (
                self.provider.__class__.__name__
                if self.provider
                else None
            ),

            "mapper": (
                self.mapper.__class__.__name__
                if self.mapper
                else None
            ),

            "candles": (
                len(self.candles)
                if self.candles
                else 0
            ),

            "duration": self.duration,

            "has_error": self.has_error,
        }
