"""
notification_formatter.py

Notification Formatter.

Author: Andrew Kyalo
Project: Andy Scanner
"""


class NotificationFormatter:
    """
    Formats notifications for different delivery channels.
    """

    # ==================================================
    # Telegram
    # ==================================================

    @staticmethod
    def telegram(notification):

        return (
            f"📡 ANDY SCANNER\n\n"
            f"Market: {notification.metadata.get('market', '-')}\n"
            f"Timeframe: {notification.metadata.get('timeframe', '-')}\n"
            f"Signal: {notification.metadata.get('direction', '-')}\n"
            f"Confidence: {notification.metadata.get('confidence', '-')}%\n\n"
            f"{notification.message}"
        )

    # ==================================================
    # WhatsApp
    # ==================================================

    @staticmethod
    def whatsapp(notification):

        return (
            f"*ANDY SCANNER*\n\n"
            f"Market: {notification.metadata.get('market', '-')}\n"
            f"Timeframe: {notification.metadata.get('timeframe', '-')}\n"
            f"Signal: {notification.metadata.get('direction', '-')}\n"
            f"Confidence: {notification.metadata.get('confidence', '-')}%\n\n"
            f"{notification.message}"
        )

    # ==================================================
    # Email
    # ==================================================

    @staticmethod
    def email(notification):

        subject = notification.title

        body = (
            f"{notification.message}\n\n"
            f"Market      : {notification.metadata.get('market', '-')}\n"
            f"Timeframe   : {notification.metadata.get('timeframe', '-')}\n"
            f"Signal      : {notification.metadata.get('direction', '-')}\n"
            f"Confidence  : {notification.metadata.get('confidence', '-')}%\n"
        )

        return {

            "subject": subject,

            "body": body,

        }

    # ==================================================
    # Console
    # ==================================================

    @staticmethod
    def console(notification):

        return (
            f"[{notification.priority}] "
            f"{notification.title} | "
            f"{notification.message}"
        )

    # ==================================================
    # Generic
    # ==================================================

    @staticmethod
    def format(notification):

        channel = notification.channel.lower()

        if channel == "telegram":

            return NotificationFormatter.telegram(notification)

        if channel == "whatsapp":

            return NotificationFormatter.whatsapp(notification)

        if channel == "email":

            return NotificationFormatter.email(notification)

        return NotificationFormatter.console(notification)