"""
telegram_notifier.py

Telegram Notification Channel.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import requests


class TelegramNotifier:
    """
    Sends notifications to Telegram.
    """

    def __init__(
        self,
        bot_token=None,
        chat_id=None,
        timeout=10,
    ):

        self.bot_token = bot_token

        self.chat_id = chat_id

        self.timeout = timeout

    # ==================================================
    # Configuration
    # ==================================================

    def configure(
        self,
        bot_token,
        chat_id,
    ):

        self.bot_token = bot_token

        self.chat_id = chat_id

    @property
    def configured(self):

        return (

            self.bot_token is not None

            and

            self.chat_id is not None

        )

    # ==================================================
    # Send Notification
    # ==================================================

    def send(
        self,
        notification,
    ):

        if not self.configured:

            raise RuntimeError(
                "TelegramNotifier is not configured."
            )

        url = (
            f"https://api.telegram.org/bot"
            f"{self.bot_token}/sendMessage"
        )

        payload = {

            "chat_id": self.chat_id,

            "text": self._format(notification),

            "parse_mode": "HTML",

        }

        response = requests.post(

            url,

            json=payload,

            timeout=self.timeout,

        )

        response.raise_for_status()

        notification.mark_sent()

        return response.json()

    # ==================================================
    # Formatting
    # ==================================================

    def _format(
        self,
        notification,
    ):

        return (

            f"<b>{notification.title}</b>\n\n"

            f"{notification.message}\n\n"

            f"<b>Priority:</b> "
            f"{notification.priority.value}\n"

            f"<b>Type:</b> "
            f"{notification.notification_type.value}"

        )