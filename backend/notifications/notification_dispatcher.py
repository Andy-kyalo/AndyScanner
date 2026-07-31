"""
notification_dispatcher.py

Notification Dispatcher.

Author: Andrew Kyalo
Project: Andy Scanner
"""


class NotificationDispatcher:
    """
    Dispatches notifications to registered channels.
    """

    def __init__(self):

        self.channels = {}

    # ==================================================
    # Channel Registration
    # ==================================================

    def register_channel(
        self,
        name,
        handler,
    ):

        self.channels[name.upper()] = handler

    def unregister_channel(
        self,
        name,
    ):

        self.channels.pop(name.upper(), None)

    # ==================================================
    # Dispatch
    # ==================================================

    def dispatch(
        self,
        notification,
    ):

        channel = notification.channel.upper()

        if channel not in self.channels:

            raise RuntimeError(
                f"No dispatcher registered for '{channel}'."
            )

        self.channels[channel](notification)

        notification.mark_sent()

        return True

    # ==================================================
    # Broadcast
    # ==================================================

    def broadcast(
        self,
        notification,
    ):

        for handler in self.channels.values():

            handler(notification)

        notification.mark_sent()

        return True

    # ==================================================
    # Information
    # ==================================================

    def registered_channels(self):

        return list(self.channels.keys())

    def channel_count(self):

        return len(self.channels)

    def has_channel(
        self,
        name,
    ):

        return name.upper() in self.channels


# ==================================================
# Default Console Dispatcher
# ==================================================

def console_dispatcher(notification):

    print()

    print("========== NOTIFICATION ==========")
    print(f"Title    : {notification.title}")
    print(f"Type     : {notification.notification_type.value}")
    print(f"Priority : {notification.priority.value}")
    print(f"Channel  : {notification.channel}")
    print(f"Message  : {notification.message}")
    print("==================================")