"""
signal_dispatcher.py

Signal Dispatcher.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime


class SignalDispatcher:
    """
    Dispatches signals to one or more output channels.
    """

    def __init__(self):

        self._channels = {}

        self.total_dispatched = 0

        self.total_failed = 0

        self.last_dispatch = None

    # ==================================================
    # Channel Registration
    # ==================================================

    def register(
        self,
        name,
        channel,
    ):

        self._channels[name] = channel

    def unregister(
        self,
        name,
    ):

        self._channels.pop(name, None)

    def channels(self):

        return list(self._channels.keys())

    # ==================================================
    # Dispatch
    # ==================================================

    def dispatch(self, signal):

        self.last_dispatch = datetime.now()

        success = True

        for name, channel in self._channels.items():

            try:

                channel.send(signal)

            except Exception:

                success = False

        if success:

            signal.dispatched()

            self.total_dispatched += 1

        else:

            signal.failed()

            self.total_failed += 1

        return success

    # ==================================================
    # Statistics
    # ==================================================

    @property
    def success_rate(self):

        total = self.total_dispatched + self.total_failed

        if total == 0:

            return 0.0

        return round(

            (self.total_dispatched / total) * 100,

            2,

        )

    def summary(self):

        return {

            "registered_channels": len(self._channels),

            "total_dispatched": self.total_dispatched,

            "total_failed": self.total_failed,

            "success_rate": self.success_rate,

            "last_dispatch": self.last_dispatch,

        }

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):

        self.total_dispatched = 0

        self.total_failed = 0

        self.last_dispatch = None