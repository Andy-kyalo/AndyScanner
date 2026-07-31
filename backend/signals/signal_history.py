"""
signal_history.py

Signal History.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from collections import deque


class SignalHistory:
    """
    Stores historical signal records.
    """

    def __init__(self, max_size=1000):

        self.max_size = max(1, int(max_size))

        self._history = deque(maxlen=self.max_size)

    # ==================================================
    # Operations
    # ==================================================

    def add(self, signal):

        self._history.append(signal)

    def clear(self):

        self._history.clear()

    # ==================================================
    # Retrieval
    # ==================================================

    def latest(self):

        if not self._history:

            return None

        return self._history[-1]

    def oldest(self):

        if not self._history:

            return None

        return self._history[0]

    def all(self):

        return list(self._history)

    def last(self, count=10):

        count = max(1, int(count))

        return list(self._history)[-count:]

    # ==================================================
    # Search
    # ==================================================

    def find(self, signal_id):

        for signal in self._history:

            if getattr(signal, "signal_id", None) == signal_id:

                return signal

        return None

    # ==================================================
    # Statistics
    # ==================================================

    def size(self):

        return len(self._history)

    def empty(self):

        return self.size() == 0

    def summary(self):

        return {

            "records": self.size(),

            "capacity": self.max_size,

            "empty": self.empty(),

        }