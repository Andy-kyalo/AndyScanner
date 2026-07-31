"""
notification.py

Notification model.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Notification:
    """
    Represents one notification.
    """

    notification_id: str

    channel: str

    title: str

    message: str

    priority: str = "NORMAL"

    created_at: datetime = field(default_factory=datetime.now)

    delivered: bool = False

    delivered_at: datetime | None = None

    metadata: dict = field(default_factory=dict)

    # ==================================================

    def mark_delivered(self):

        self.delivered = True

        self.delivered_at = datetime.now()

    # ==================================================

    def to_dict(self):

        return {

            "notification_id": self.notification_id,

            "channel": self.channel,

            "title": self.title,

            "message": self.message,

            "priority": self.priority,

            "created_at": self.created_at,

            "delivered": self.delivered,

            "delivered_at": self.delivered_at,

            "metadata": self.metadata,

        }