import unittest
from unittest.mock import Mock, patch

import main


class TestMainReportingRecovery(unittest.TestCase):

    def test_scan_report_failure_does_not_skip_database_report(self):
        report = Mock()
        report.print_scan_report.side_effect = RuntimeError(
            "scan report failed"
        )

        with patch("main.logger.error_log") as log_error:
            main.print_reports_safely(
                report,
                [],
                object(),
                object(),
            )

        report.print_scan_report.assert_called_once()
        report.print_database_report.assert_called_once()
        log_error.assert_called_once()

    def test_database_report_failure_is_logged(self):
        report = Mock()
        report.print_database_report.side_effect = RuntimeError(
            "database report failed"
        )

        with patch("main.logger.error_log") as log_error:
            main.print_reports_safely(
                report,
                [],
                object(),
                object(),
            )

        report.print_scan_report.assert_called_once()
        report.print_database_report.assert_called_once()
        log_error.assert_called_once()

    def test_logging_failure_does_not_escape_recovery(self):
        report = Mock()
        report.print_scan_report.side_effect = RuntimeError(
            "scan report failed"
        )

        with patch(
            "main.logger.error_log",
            side_effect=OSError("logger unavailable"),
        ):
            main.print_reports_safely(
                report,
                [],
                object(),
                object(),
            )

        report.print_database_report.assert_called_once()


if __name__ == "__main__":
    unittest.main()
