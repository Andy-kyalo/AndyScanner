"""
signal_manager.py

Signal Manager.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.signals.signal_context import SignalContext
from backend.signals.signal_queue import SignalQueue
from backend.signals.signal_dispatcher import SignalDispatcher
from backend.signals.signal_history import SignalHistory
from backend.signals.signal_metrics import SignalMetrics


class SignalManager:
    """
    Central manager for the Signal subsystem.
    """

    def __init__(self):

        self.queue = SignalQueue()

        self.dispatcher = SignalDispatcher()

        self.history = SignalHistory()

        self.metrics = SignalMetrics()

    # ==================================================
    # Signal Creation
    # ==================================================

    def create_signal(
        self,
        signal_id,
        market,
        timeframe,
        direction,
        confidence,
    ):

        context = SignalContext()

        context.create(
            signal_id,
            market,
            timeframe,
            direction,
            confidence,
        )

        self.metrics.signal_generated()

        return context

    # ==================================================
    # Queue
    # ==================================================

    def enqueue(self, signal):

        status = self.queue.enqueue(signal)

        if status:

            self.metrics.signal_queued()

        return status

    # ==================================================
    # Dispatch
    # ==================================================

    def dispatch_next(self):

        signal = self.queue.dequeue()

        if signal is None:

            return None

        status = self.dispatcher.dispatch(signal)

        if status:

            self.metrics.signal_dispatched()

        else:

            self.metrics.signal_failed()

        self.history.add(signal)

        return signal

    # ==================================================
    # Registration
    # ==================================================

    def register_channel(
        self,
        name,
        channel,
    ):

        self.dispatcher.register(
            name,
            channel,
        )

    def unregister_channel(self, name):

        self.dispatcher.unregister(name)

    # ==================================================
    # Information
    # ==================================================

    def summary(self):

        return {

            "queue": self.queue.summary(),

            "dispatcher": self.dispatcher.summary(),

            "history": self.history.summary(),

            "metrics": self.metrics.summary(),

        }

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):

        self.queue.clear()

        self.history.clear()

        self.metrics.reset()

        self.dispatcher.reset()