"""
signal_queue.py

Signal Queue.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from threading import Lock


class SignalQueue:
    """
    Thread-safe queue for pending signals.
    """

    def __init__(self):

        self._queue = []

        self._lock = Lock()

    # ==================================================
    # Queue Operations
    # ==================================================

    def enqueue(self, context):

        with self._lock:

            for signal in self._queue:

                if signal.signal_id == context.signal_id:

                    return False

            context.queue()

            self._queue.append(context)

            return True

    def dequeue(self):

        with self._lock:

            if not self._queue:

                return None

            signal = self._queue.pop(0)

            signal.processing()

            return signal

    def peek(self):

        with self._lock:

            if not self._queue:

                return None

            return self._queue[0]

    def clear(self):

        with self._lock:

            self._queue.clear()

    # ==================================================
    # Search
    # ==================================================

    def find(self, signal_id):

        with self._lock:

            for signal in self._queue:

                if signal.signal_id == signal_id:

                    return signal

        return None

    def remove(self, signal_id):

        with self._lock:

            for signal in self._queue:

                if signal.signal_id == signal_id:

                    self._queue.remove(signal)

                    return True

        return False

    # ==================================================
    # Information
    # ==================================================

    def size(self):

        return len(self._queue)

    def empty(self):

        return self.size() == 0

    def signals(self):

        with self._lock:

            return list(self._queue)

    def summary(self):

        return {

            "queue_size": self.size(),

            "empty": self.empty(),

        }