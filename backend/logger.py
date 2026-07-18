"""
logger.py

Professional logging system for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import os
import logging


class Logger:

    # ==========================================
    # Constructor
    # ==========================================

    def __init__(self):

        # Create logs directory
        os.makedirs("logs", exist_ok=True)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # ===========================
        # Scanner Logger
        # ===========================

        self.scanner = logging.getLogger("Scanner")
        self.scanner.setLevel(logging.INFO)

        if not self.scanner.handlers:

            file_handler = logging.FileHandler("logs/scanner.log")
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            self.scanner.addHandler(file_handler)
            self.scanner.addHandler(console_handler)

        # ===========================
        # Signal Logger
        # ===========================

        self.signal = logging.getLogger("Signal")
        self.signal.setLevel(logging.INFO)

        if not self.signal.handlers:

            file_handler = logging.FileHandler("logs/signals.log")
            file_handler.setFormatter(formatter)

            self.signal.addHandler(file_handler)

        # ===========================
        # Error Logger
        # ===========================

        self.error = logging.getLogger("Error")
        self.error.setLevel(logging.ERROR)

        if not self.error.handlers:

            file_handler = logging.FileHandler("logs/errors.log")
            file_handler.setFormatter(formatter)

            self.error.addHandler(file_handler)

        # ===========================
        # Session Logger
        # ===========================

        self.session = logging.getLogger("Session")
        self.session.setLevel(logging.INFO)

        if not self.session.handlers:

            file_handler = logging.FileHandler("logs/sessions.log")
            file_handler.setFormatter(formatter)

            self.session.addHandler(file_handler)

    # ==========================================
    # General Info Logger
    # ==========================================

    def info(self, logger_name, message):

        if logger_name == "Scanner":
            self.scanner.info(message)

        elif logger_name == "Signal":
            self.signal.info(message)

        elif logger_name == "Session":
            self.session.info(message)

        else:
            self.scanner.info(message)

    # ==========================================
    # Error Logger
    # ==========================================

    def error_log(self, message):
        self.error.error(message)

    # ==========================================
    # Scanner Logger
    # ==========================================

    def scanner_log(self, message):
        self.scanner.info(message)

    # ==========================================
    # Signal Logger
    # ==========================================

    def signal_log(self, message):
        self.signal.info(message)

    # ==========================================
    # Session Logger
    # ==========================================

    def session_log(self, message):
        self.session.info(message)


# ==========================================
# Global Logger Instance
# ==========================================

logger = Logger()