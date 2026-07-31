"""
notification_metrics.py

Notification Metrics.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime


class NotificationMetrics:
    """
    Collects notification subsystem metrics.
    """

    def __init__(self):

        self.started_at = datetime.now()

        self.total_notifications = 0

        self.successful_notifications = 0

        self.failed_notifications = 0

        self.disabled_notifications = 0

        self.last_notification = None

    # ==================================================
    # Counters
    # ==================================================

    def notification_created(self):

        self.total_notifications += 1

        self.last_notification = datetime.now()

    def notification_sent(self):

        self.successful_notifications += 1

    def notification_failed(self):

        self.failed_notifications += 1

    def notification_disabled(self):

        self.disabled_notifications += 1

    # ==================================================
    # Statistics
    # ==================================================

    @property
    def success_rate(self):

        total = (
            self.successful_notifications
            + self.failed_notifications
        )

        if total == 0:

            return 0.0

        return round(

            (self.successful_notifications / total) * 100,

            2,

        )

    @property
    def uptime(self):

        return round(

            (
                datetime.now()
                - self.started_at
            ).total_seconds(),

            2,

        )

    # ==================================================
    # Export
    # ==================================================

    def summary(self):

        return {

            "total_notifications": self.total_notifications,

            "successful_notifications": self.successful_notifications,

            "failed_notifications": self.failed_notifications,

            "disabled_notifications": self.disabled_notifications,

            "success_rate": self.success_rate,

            "uptime": self.uptime,

            "last_notification": self.last_notification,

        }

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):

        self.__init__()