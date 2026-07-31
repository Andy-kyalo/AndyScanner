"""
notification_channel.py

Notification Channel Interface.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from abc import ABC
from abc import abstractmethod


class NotificationChannel(ABC):
    """
    Base class for all notification channels.
    """

    def __init__(self, name):

        self.name = name

        self.enabled = True

    # ==================================================
    # Channel Status
    # ==================================================

    def enable(self):

        self.enabled = True

    def disable(self):

        self.enabled = False

    @property
    def active(self):

        return self.enabled

    # ==================================================
    # Send
    # ==================================================

    @abstractmethod
    def send(self, notification):
        """
        Send notification through this channel.
        """
        raise NotImplementedError

    # ==================================================
    # Information
    # ==================================================

    def summary(self):

        return {

            "name": self.name,

            "enabled": self.enabled,

        }