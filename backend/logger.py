"""
logger.py

Professional logging system for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import logging
import os


class Logger:
    """
    Professional logging manager for Andy Scanner.
    """

    LOG_DIRECTORY = "logs"

    def __init__(self):
        """
        Initialize all project loggers.
        """

        os.makedirs(self.LOG_DIRECTORY, exist_ok=True)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        self.scanner = self._create_logger(
            "Scanner",
            "scanner.log",
            logging.INFO,
            formatter,
            console_output=True,
        )

        self.signal = self._create_logger(
            "Signal",
            "signals.log",
            logging.INFO,
            formatter,
        )

        self.error = self._create_logger(
            "Error",
            "errors.log",
            logging.ERROR,
            formatter,
        )

        self.session = self._create_logger(
            "Session",
            "sessions.log",
            logging.INFO,
            formatter,
        )

    # ==========================================================
    # INTERNAL LOGGER CREATOR
    # ==========================================================

    def _create_logger(
        self,
        name,
        filename,
        level,
        formatter,
        console_output=False,
    ):
        """
        Create and configure a logger.
        """

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.propagate = False

        if not logger.handlers:

            file_handler = logging.FileHandler(
                os.path.join(self.LOG_DIRECTORY, filename),
                encoding="utf-8",
            )

            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            if console_output:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)

        return logger

    # ==========================================================
    # GENERAL LOGGING
    # ==========================================================

    def info(self, logger_name, message):
        """
        Write an INFO message to the selected logger.
        """

        loggers = {
            "Scanner": self.scanner,
            "Signal": self.signal,
            "Session": self.session,
        }

        loggers.get(logger_name, self.scanner).info(message)

    # ==========================================================
    # SPECIALIZED LOGGERS
    # ==========================================================

    def scanner_log(self, message):
        """Write scanner log."""
        self.scanner.info(message)

    def signal_log(self, message):
        """Write signal log."""
        self.signal.info(message)

    def session_log(self, message):
        """Write session log."""
        self.session.info(message)

    def error_log(self, message):
        """Write error log."""
        self.error.error(message)


# ==========================================================
# Global Logger Instance
# ==========================================================

logger = Logger()