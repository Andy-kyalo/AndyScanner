"""
notification_history.py

Notification History.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from copy import deepcopy


class NotificationHistory:
    """
    Stores all dispatched notifications.
    """

    def __init__(self):

        self._history = []

    # ==================================================
    # Store
    # ==================================================

    def add(
        self,
        notification,
    ):

        self._history.append(notification)

    # ==================================================
    # Queries
    # ==================================================

    def all(self):

        return list(self._history)

    def latest(self):

        if not self._history:
            return None

        return self._history[-1]

    def count(self):

        return len(self._history)

    def sent(self):

        return [
            notification
            for notification in self._history
            if notification.sent
        ]

    def pending(self):

        return [
            notification
            for notification in self._history
            if not notification.sent
        ]

    # ==================================================
    # Search
    # ==================================================

    def by_channel(
        self,
        channel,
    ):

        channel = channel.upper()

        return [
            notification
            for notification in self._history
            if notification.channel.upper() == channel
        ]

    def by_type(
        self,
        notification_type,
    ):

        value = (
            notification_type.value
            if hasattr(notification_type, "value")
            else str(notification_type)
        )

        return [
            notification
            for notification in self._history
            if notification.notification_type.value == value
        ]

    def by_priority(
        self,
        priority,
    ):

        value = (
            priority.value
            if hasattr(priority, "value")
            else str(priority)
        )

        return [
            notification
            for notification in self._history
            if notification.priority.value == value
        ]

    # ==================================================
    # Export
    # ==================================================

    def export(self):

        return [
            deepcopy(notification.to_dict())
            for notification in self._history
        ]

    # ==================================================
    # Maintenance
    # ==================================================

    def clear(self):

        self._history.clear()