"""
test_market_data_integrity.py

Regression tests for timestamp normalization, ordering,
and market-data freshness.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import unittest
from datetime import datetime, timedelta, timezone

from backend.validation.validators.duplicate_candles import (
    DuplicateCandlesValidator,
)
from backend.validation.validators.freshness_validator import (
    FreshnessValidator,
)


class Candle:
    def __init__(self, timestamp):
        self.time = timestamp


class TestDuplicateCandlesValidator(unittest.TestCase):

    def setUp(self):
        self.validator = DuplicateCandlesValidator()

    def test_duplicate_string_timestamps_are_rejected(self):
        candles = [
            Candle("2026-10-09 10:00:00"),
            Candle("2026-10-09T10:00:00"),
        ]

        valid, message = self.validator.validate(candles)

        self.assertFalse(valid)
        self.assertIn("Duplicate candle", message)

    def test_timezone_equivalent_timestamps_are_rejected(self):
        candles = [
            Candle("2026-10-09 10:00:00"),
            Candle(datetime(
                2026, 10, 9, 12, 0,
                tzinfo=timezone(timedelta(hours=2)),
            )),
        ]

        valid, message = self.validator.validate(candles)

        self.assertFalse(valid)
        self.assertIn("Duplicate candle", message)

    def test_distinct_timestamps_pass(self):
        candles = [
            Candle("2026-10-09 10:00:00"),
            Candle("2026-10-09 10:05:00"),
        ]

        valid, message = self.validator.validate(candles)

        self.assertTrue(valid, message)
    def test_iso_timezone_equivalent_strings_are_duplicates(self):
        candles = [
            Candle("2026-10-09T12:00:00+02:00"),
            Candle("2026-10-09T10:00:00Z"),
        ]

        valid, message = self.validator.validate(candles)

        self.assertFalse(valid)
        self.assertIn("Duplicate candle", message)


class TestFreshnessValidator(unittest.TestCase):

    def setUp(self):
        self.validator = FreshnessValidator()
        self.now = datetime(
            2026, 10, 9, 10, 20,
            tzinfo=timezone.utc,
        )

    def test_out_of_order_candles_are_rejected(self):
        candles = [
            Candle("2026-10-09 10:15:00"),
            Candle("2026-10-09 10:10:00"),
        ]

        valid, message = self.validator.validate(
            candles,
            "M5",
            now=self.now,
        )

        self.assertFalse(valid)
        self.assertIn("chronological order", message)

    def test_future_latest_candle_is_rejected(self):
        candles = [
            Candle("2026-10-09 10:15:00"),
            Candle("2026-10-09 10:25:00"),
        ]

        valid, message = self.validator.validate(
            candles,
            "M5",
            now=self.now,
        )

        self.assertFalse(valid)
        self.assertIn("in the future", message)

    def test_stale_data_is_rejected(self):
        candles = [
            Candle("2026-10-09 10:00:00"),
        ]

        valid, message = self.validator.validate(
            candles,
            "M5",
            now=self.now,
        )

        self.assertFalse(valid)
        self.assertIn("stale", message)

    def test_exact_freshness_boundary_is_accepted(self):
        candles = [
            Candle("2026-10-09 10:10:00"),
        ]

        valid, message = self.validator.validate(
            candles,
            "M5",
            now=self.now,
        )

        self.assertTrue(valid, message)

    def test_iso_utc_timestamp_is_supported(self):
        candles = [Candle("2026-10-09T10:15:00Z")]

        valid, message = self.validator.validate(
            candles, "M5", now=self.now
        )

        self.assertTrue(valid, message)

    def test_iso_offset_timestamp_is_supported(self):
        candles = [Candle("2026-10-09T12:15:00+02:00")]

        valid, message = self.validator.validate(
            candles, "M5", now=self.now
        )

        self.assertTrue(valid, message)

    def test_invalid_multiplier_is_rejected(self):
        candles = [
            Candle("2026-10-09 10:15:00"),
        ]

        valid, message = self.validator.validate(
            candles,
            "M5",
            now=self.now,
            multiplier=0,
        )

        self.assertFalse(valid)
        self.assertIn("positive number", message)


if __name__ == "__main__":
    unittest.main()
