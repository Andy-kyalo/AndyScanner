import logging
import unittest
from unittest.mock import Mock

from backend.logger import Logger


class TestLoggerRedaction(unittest.TestCase):

    def test_all_public_logging_methods_redact_secrets(self):
        logger = Logger.__new__(Logger)
        logger.scanner = Mock()
        logger.signal = Mock()
        logger.session = Mock()
        logger.error = Mock()

        secret = "SYNTHETIC_LOG_SECRET_123"
        message = f"Request failed: apikey={secret}"

        logger.info("Scanner", message)
        logger.scanner_log(message)
        logger.signal_log(message)
        logger.session_log(message)
        logger.error_log(message)

        calls = [
            logger.scanner.info.call_args.args[0],
            logger.scanner.info.call_args.args[0],
            logger.signal.info.call_args.args[0],
            logger.session.info.call_args.args[0],
            logger.error.error.call_args.args[0],
        ]

        for logged_message in calls:
            with self.subTest(message=logged_message):
                self.assertNotIn(secret, logged_message)
                self.assertIn("[REDACTED]", logged_message)

    def test_non_secret_message_is_preserved(self):
        message = "Provider timeout after 10 seconds"
        self.assertEqual(Logger._safe_message(message), message)


if __name__ == "__main__":
    unittest.main()
