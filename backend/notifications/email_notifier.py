"""
email_notifier.py

Email Notification Channel.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailNotifier:
    """
    Sends notifications through SMTP email.
    """

    def __init__(
        self,
        smtp_server=None,
        smtp_port=587,
        username=None,
        password=None,
        sender=None,
        recipient=None,
    ):

        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

        self.username = username
        self.password = password

        self.sender = sender
        self.recipient = recipient

    # ==================================================
    # Configuration
    # ==================================================

    def configure(
        self,
        smtp_server,
        smtp_port,
        username,
        password,
        sender,
        recipient,
    ):

        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

        self.username = username
        self.password = password

        self.sender = sender
        self.recipient = recipient

    @property
    def configured(self):

        return all(
            [
                self.smtp_server,
                self.username,
                self.password,
                self.sender,
                self.recipient,
            ]
        )

    # ==================================================
    # Send
    # ==================================================

    def send(
        self,
        notification,
    ):

        if not self.configured:

            raise RuntimeError(
                "EmailNotifier is not configured."
            )

        message = MIMEMultipart()

        message["From"] = self.sender
        message["To"] = self.recipient
        message["Subject"] = notification.title

        message.attach(
            MIMEText(
                self._format(notification),
                "plain",
            )
        )

        with smtplib.SMTP(
            self.smtp_server,
            self.smtp_port,
        ) as server:

            server.starttls()

            server.login(
                self.username,
                self.password,
            )

            server.sendmail(
                self.sender,
                self.recipient,
                message.as_string(),
            )

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
            f"{notification.title}\n\n"
            f"{notification.message}\n\n"
            f"Priority : {notification.priority.value}\n"
            f"Type     : {notification.notification_type.value}\n"
            f"Channel  : {notification.channel}"
        )