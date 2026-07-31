"""
notification_statistics.py

Notification Statistics.

Author: Andrew Kyalo
Project: Andy Scanner
"""


class NotificationStatistics:
    """
    Computes statistics for notification history.
    """

    def __init__(self, history):

        self.history = history

    # ==================================================
    # Totals
    # ==================================================

    def total(self):

        return self.history.count()

    def sent(self):

        return len(self.history.sent())

    def pending(self):

        return len(self.history.pending())

    # ==================================================
    # Success Rate
    # ==================================================

    def success_rate(self):

        total = self.total()

        if total == 0:
            return 0.0

        return round(
            (self.sent() / total) * 100,
            2,
        )

    # ==================================================
    # Group By Channel
    # ==================================================

    def channels(self):

        result = {}

        for notification in self.history.all():

            channel = notification.channel.upper()

            result[channel] = result.get(channel, 0) + 1

        return result

    # ==================================================
    # Group By Type
    # ==================================================

    def types(self):

        result = {}

        for notification in self.history.all():

            notification_type = (
                notification.notification_type.value
            )

            result[notification_type] = (
                result.get(notification_type, 0) + 1
            )

        return result

    # ==================================================
    # Group By Priority
    # ==================================================

    def priorities(self):

        result = {}

        for notification in self.history.all():

            priority = notification.priority.value

            result[priority] = (
                result.get(priority, 0) + 1
            )

        return result

    # ==================================================
    # Complete Report
    # ==================================================

    def report(self):

        return {

            "total": self.total(),

            "sent": self.sent(),

            "pending": self.pending(),

            "success_rate": self.success_rate(),

            "channels": self.channels(),

            "types": self.types(),

            "priorities": self.priorities(),
        }