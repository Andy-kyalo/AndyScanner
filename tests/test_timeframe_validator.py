"""
test_timeframe_validator.py

Regression tests for the production TimeframeValidator.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import unittest
from datetime import datetime, timedelta, timezone

from backend.candle import Candle
from backend.validation.validators.timeframe_validator import (
    TimeframeValidator,
)


class TestTimeframeValidator(unittest.TestCase):

    def setUp(self):
        self.validator = TimeframeValidator()

    @staticmethod
    def make_candles(times):
        return [
            Candle(
                time=timestamp,
                open_price=100,
                high=102,
                low=98,
                close=101,
            )
            for timestamp in times
        ]

    def test_valid_chronological_candles_pass(self):
        start = datetime(
            2026, 10, 9, 8, 0,
            tzinfo=timezone.utc,
        )

        candles = self.make_candles([
            start.strftime("%Y-%m-%d %H:%M:%S"),
            (start + timedelta(minutes=5)).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            (start + timedelta(minutes=10)).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        ])

        valid, message = self.validator.validate(
            candles, "M5"
        )

        self.assertTrue(valid, message)
        self.assertEqual(
            message,
            "Timeframe validation passed.",
        )

    def test_reverse_chronological_order_is_rejected(self):
        start = datetime(
            2026, 10, 9, 8, 10,
            tzinfo=timezone.utc,
        )

        candles = self.make_candles([
            start.strftime("%Y-%m-%d %H:%M:%S"),
            (start - timedelta(minutes=5)).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        ])

        valid, message = self.validator.validate(
            candles, "M5"
        )

        self.assertFalse(valid)
        self.assertIn(
            "chronological order",
            message,
        )

    def test_duplicate_timestamps_are_rejected(self):
        timestamp = "2026-10-09 08:00:00"
        candles = self.make_candles([
            timestamp,
            timestamp,
        ])

        valid, message = self.validator.validate(
            candles, "M5"
        )

        self.assertFalse(valid)
        self.assertIn(
            "chronological order",
            message,
        )

    def test_incorrect_timeframe_gap_is_rejected(self):
        candles = self.make_candles([
            "2026-10-09 08:00:00",
            "2026-10-09 08:06:00",
        ])

        valid, message = self.validator.validate(
            candles, "M5"
        )

        self.assertFalse(valid)
        self.assertIn(
            "Invalid timeframe gap",
            message,
        )

    def test_unsupported_timeframe_is_rejected(self):
        candles = self.make_candles([
            "2026-10-09 08:00:00",
            "2026-10-09 08:05:00",
        ])

        valid, message = self.validator.validate(
            candles, "M7"
        )

        self.assertFalse(valid)
        self.assertIn(
            "Unsupported timeframe",
            message,
        )

    def test_unsupported_timestamp_format_is_rejected(self):
        candles = self.make_candles([
            "08:00",
            "08:05",
        ])

        valid, message = self.validator.validate(
            candles, "M5"
        )

        self.assertFalse(valid)
        self.assertIn(
            "Unsupported candle timestamp format",
            message,
        )

    def test_datetime_objects_are_supported(self):
        start = datetime(
            2026, 10, 9, 8, 0,
            tzinfo=timezone.utc,
        )

        candles = self.make_candles([
            start,
            start + timedelta(minutes=5),
        ])

        valid, message = self.validator.validate(
            candles, "M5"
        )

        self.assertTrue(valid, message)

    def test_single_candle_does_not_require_spacing_check(self):
        candles = self.make_candles([
            "2026-10-09 08:00:00",
        ])

        valid, message = self.validator.validate(
            candles, "M5"
        )

        self.assertTrue(valid, message)
    def test_iso_timezone_offset_timestamps_are_supported(self):
        candles = self.make_candles([
            "2026-10-09T10:00:00Z",
            "2026-10-09T12:05:00+02:00",
        ])

        valid, message = self.validator.validate(candles, "M5")

        self.assertTrue(valid, message)



if __name__ == "__main__":
    unittest.main()
