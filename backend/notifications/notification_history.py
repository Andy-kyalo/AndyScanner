"""
notification_history.py

Notification History.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from collections import deque


class NotificationHistory:
    """
    Stores notification history.
    """

    def __init__(self, max_size=1000):

        self.max_size = max(1, int(max_size))

        self._history = deque(maxlen=self.max_size)

    # ==================================================
    # Operations
    # ==================================================

    def add(self, notification):

        self._history.append(notification)

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

    def find(self, notification_id):

        for notification in self._history:

            if getattr(notification, "notification_id", None) == notification_id:

                return notification

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