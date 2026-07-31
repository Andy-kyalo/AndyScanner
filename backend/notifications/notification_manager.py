"""
notification_manager.py

Notification Manager.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.notifications.notification_history import NotificationHistory
from backend.notifications.notification_metrics import NotificationMetrics


class NotificationManager:
    """
    Central notification coordinator.
    """

    def __init__(self):

        self.channels = {}

        self.history = NotificationHistory()

        self.metrics = NotificationMetrics()

    # ==================================================
    # Channel Management
    # ==================================================

    def register_channel(
        self,
        name,
        channel,
    ):

        self.channels[name] = channel

    def unregister_channel(self, name):

        self.channels.pop(name, None)

    def get_channel(self, name):

        return self.channels.get(name)

    # ==================================================
    # Send Notification
    # ==================================================

    def send(self, notification):

        self.metrics.notification_created()

        channel = self.channels.get(notification.channel)

        if channel is None:

            self.metrics.notification_failed()

            return False

        if not channel.active:

            self.metrics.notification_disabled()

            return False

        try:

            status = channel.send(notification)

            if status:

                notification.mark_delivered()

                self.metrics.notification_sent()

            else:

                self.metrics.notification_failed()

            self.history.add(notification)

            return status

        except Exception:

            self.metrics.notification_failed()

            return False

    # ==================================================
    # Broadcast
    # ==================================================

    def broadcast(self, notification):

        delivered = 0

        for channel in self.channels.values():

            clone = type(notification)(**notification.to_dict())

            clone.channel = channel.name

            if self.send(clone):

                delivered += 1

        return delivered

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):

        self.history.clear()

        self.metrics.reset()

    # ==================================================
    # Information
    # ==================================================

    def summary(self):

        return {

            "channels": list(self.channels.keys()),

            "history": self.history.summary(),

            "metrics": self.metrics.summary(),

        }