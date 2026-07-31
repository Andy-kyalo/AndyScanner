"""
desktop_notifier.py

Desktop Notification Channel.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import platform
import subprocess


class DesktopNotifier:
    """
    Sends desktop notifications.

    Works on Linux/Termux (when available),
    and is easily extendable for Windows/macOS.
    """

    def __init__(self):

        self.system = platform.system()

    # ==================================================
    # Send
    # ==================================================

    def send(
        self,
        notification,
    ):

        title = notification.title

        message = self._format(notification)

        try:

            if self.system == "Linux":

                subprocess.run(
                    [
                        "termux-notification",
                        "--title",
                        title,
                        "--content",
                        message,
                    ],
                    check=False,
                )

            elif self.system == "Windows":

                pass

            elif self.system == "Darwin":

                pass

        except Exception:

            return False

        notification.mark_sent()

        return True

    # ==================================================
    # Formatter
    # ==================================================

    def _format(
        self,
        notification,
    ):

        return (
            f"{notification.message}\n\n"
            f"Priority : {notification.priority.value}\n"
            f"Type     : {notification.notification_type.value}"
        )