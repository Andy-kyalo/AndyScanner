"""
Professional logging system for Andy Scanner.
"""

import logging
import os

from backend.log_redaction import redact_secrets


class Logger:
    """Professional logging manager for Andy Scanner."""

    LOG_DIRECTORY = "logs"

    def __init__(self):
        os.makedirs(self.LOG_DIRECTORY, exist_ok=True)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        self.scanner = self._create_logger(
            "Scanner", "scanner.log", logging.INFO, formatter,
            console_output=True,
        )
        self.signal = self._create_logger(
            "Signal", "signals.log", logging.INFO, formatter,
        )
        self.error = self._create_logger(
            "Error", "errors.log", logging.ERROR, formatter,
        )
        self.session = self._create_logger(
            "Session", "sessions.log", logging.INFO, formatter,
        )

    def _create_logger(
        self, name, filename, level, formatter, console_output=False
    ):
        """Create and configure a logger."""
        target = logging.getLogger(name)
        target.setLevel(level)
        target.propagate = False

        if not target.handlers:
            file_handler = logging.FileHandler(
                os.path.join(self.LOG_DIRECTORY, filename),
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
            target.addHandler(file_handler)

            if console_output:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                target.addHandler(console_handler)

        return target

    @staticmethod
    def _safe_message(message):
        """Redact credentials before a message reaches a logger."""
        return redact_secrets(message)

    def info(self, logger_name, message):
        """Write a redacted INFO message to the selected logger."""
        loggers = {
            "Scanner": self.scanner,
            "Signal": self.signal,
            "Session": self.session,
        }
        loggers.get(logger_name, self.scanner).info(
            self._safe_message(message)
        )

    def scanner_log(self, message):
        """Write a redacted scanner log message."""
        self.scanner.info(self._safe_message(message))

    def signal_log(self, message):
        """Write a redacted signal log message."""
        self.signal.info(self._safe_message(message))

    def session_log(self, message):
        """Write a redacted session log message."""
        self.session.info(self._safe_message(message))

    def error_log(self, message):
        """Write a redacted error log message."""
        self.error.error(self._safe_message(message))


logger = Logger()
