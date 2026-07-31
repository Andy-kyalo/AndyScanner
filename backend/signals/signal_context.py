"""
signal_context.py

Signal execution context.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime

from backend.signals.signal_state import SignalState


class SignalContext:
    """
    Holds the complete lifecycle information of a signal.
    """

    def __init__(self):

        self.signal_id = None

        self.market = None
        self.timeframe = None

        self.direction = None
        self.confidence = 0.0

        self.created_at = None
        self.updated_at = None
        self.dispatched_at = None

        self.state = SignalState.CREATED

        self.metadata = {}

    # ==================================================
    # Lifecycle
    # ==================================================

    def create(
        self,
        signal_id,
        market,
        timeframe,
        direction,
        confidence,
    ):

        now = datetime.now()

        self.signal_id = signal_id

        self.market = market
        self.timeframe = timeframe

        self.direction = direction
        self.confidence = confidence

        self.created_at = now
        self.updated_at = now

        self.state = SignalState.CREATED

    def queue(self):

        self.state = SignalState.QUEUED

        self.updated_at = datetime.now()

    def processing(self):

        self.state = SignalState.PROCESSING

        self.updated_at = datetime.now()

    def dispatched(self):

        now = datetime.now()

        self.state = SignalState.DISPATCHED

        self.updated_at = now
        self.dispatched_at = now

    def failed(self):

        self.state = SignalState.FAILED

        self.updated_at = datetime.now()

    def expired(self):

        self.state = SignalState.EXPIRED

        self.updated_at = datetime.now()

    def cancelled(self):

        self.state = SignalState.CANCELLED

        self.updated_at = datetime.now()

    def reset(self):

        self.__init__()

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
    def active(self):

        return self.state in (
            SignalState.CREATED,
            SignalState.QUEUED,
            SignalState.PROCESSING,
        )

    @property
    def completed(self):

        return self.state == SignalState.DISPATCHED

    @property
    def failed_state(self):

        return self.state == SignalState.FAILED

    # ==================================================
    # Export
    # ==================================================

    def summary(self):

        return {

            "signal_id": self.signal_id,

            "market": self.market,

            "timeframe": self.timeframe,

            "direction": self.direction,

            "confidence": self.confidence,

            "state": self.state.value,

            "created_at": self.created_at,

            "updated_at": self.updated_at,

            "dispatched_at": self.dispatched_at,

            "metadata": dict(self.metadata),

        }