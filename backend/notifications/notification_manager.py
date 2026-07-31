"""
notification_manager.py

Central Notification Manager.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.notifications.notification import (
    Notification,
    NotificationPriority,
    NotificationType,
)


class NotificationManager:
    """
    Central manager for all notifications.
    """

    def __init__(self):

        self.notifications = []

    # ==================================================
    # Create Notification
    # ==================================================

    def create(
        self,
        title,
        message,
        notification_type=NotificationType.INFO,
        priority=NotificationPriority.NORMAL,
        channel="SYSTEM",
        metadata=None,
    ):

        notification = Notification(
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            channel=channel,
            metadata=metadata,
        )

        self.notifications.append(notification)

        return notification

    # ==================================================
    # Register Existing Notification
    # ==================================================

    def register(
        self,
        notification,
    ):

        self.notifications.append(notification)

    # ==================================================
    # Mark As Sent
    # ==================================================

    def mark_sent(
        self,
        notification,
    ):

        notification.mark_sent()

    # ==================================================
    # Queries
    # ==================================================

    def all(self):

        return list(self.notifications)

    def pending(self):

        return [
            notification
            for notification in self.notifications
            if not notification.sent
        ]

    def sent(self):

        return [
            notification
            for notification in self.notifications
            if notification.sent
        ]

    def count(self):

        return len(self.notifications)

    def pending_count(self):

        return len(self.pending())

    def sent_count(self):

        return len(self.sent())

    # ==================================================
    # Statistics
    # ==================================================

    def statistics(self):

        return {

            "total": self.count(),

            "pending": self.pending_count(),

            "sent": self.sent_count(),
        }

    # ==================================================
    # Clear
    # ==================================================

    def clear(self):

        self.notifications.clear()