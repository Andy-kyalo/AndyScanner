import unittest

from backend.candle import Candle
from backend.fvg_detector import FVGDetector


class TestFVGDetector(unittest.TestCase):

    def bullish_candles(self):

        return [
            Candle("09:00", 100, 102, 99, 101),
            Candle("10:00", 101, 108, 100, 107),
            Candle("11:00", 107, 110, 104, 109),
        ]

    def bearish_candles(self):

        return [
            Candle("09:00", 110, 112, 108, 109),
            Candle("10:00", 109, 110, 103, 104),
            Candle("11:00", 104, 106, 100, 101),
        ]

    # ==================================================
    # Validation
    # ==================================================

    def test_requires_at_least_three_candles(self):

        candles = [
            Candle("09:00", 100, 102, 99, 101),
            Candle("10:00", 101, 103, 100, 102),
        ]

        with self.assertRaises(ValueError):
            FVGDetector(candles)

    # ==================================================
    # Bullish FVG
    # ==================================================

    def test_bullish_fvg_returns_list(self):

        detector = FVGDetector(
            self.bullish_candles()
        )

        result = detector.bullish_fvg()

        self.assertIsInstance(result, list)

    def test_bullish_fvg_contains_correct_type(self):

        detector = FVGDetector(
            self.bullish_candles()
        )

        gaps = detector.bullish_fvg()

        for gap in gaps:
            self.assertEqual(
                gap["type"],
                "BULLISH",
            )

    # ==================================================
    # Bearish FVG
    # ==================================================

    def test_bearish_fvg_returns_list(self):

        detector = FVGDetector(
            self.bearish_candles()
        )

        result = detector.bearish_fvg()

        self.assertIsInstance(result, list)

    def test_bearish_fvg_contains_correct_type(self):

        detector = FVGDetector(
            self.bearish_candles()
        )

        gaps = detector.bearish_fvg()

        for gap in gaps:
            self.assertEqual(
                gap["type"],
                "BEARISH",
            )

    # ==================================================
    # FVG Structure
    # ==================================================

    def test_bullish_fvg_has_required_fields(self):

        detector = FVGDetector(
            self.bullish_candles()
        )

        gaps = detector.bullish_fvg()

        for gap in gaps:

            self.assertIn("first", gap)
            self.assertIn("middle", gap)
            self.assertIn("third", gap)

            self.assertIn("gap_top", gap)
            self.assertIn("gap_bottom", gap)
            self.assertIn("gap_size", gap)

    def test_bearish_fvg_has_required_fields(self):

        detector = FVGDetector(
            self.bearish_candles()
        )

        gaps = detector.bearish_fvg()

        for gap in gaps:

            self.assertIn("first", gap)
            self.assertIn("middle", gap)
            self.assertIn("third", gap)

            self.assertIn("gap_top", gap)
            self.assertIn("gap_bottom", gap)
            self.assertIn("gap_size", gap)

    # ==================================================
    # Latest FVG
    # ==================================================

    def test_latest_bullish_fvg_returns_gap_or_none(self):

        detector = FVGDetector(
            self.bullish_candles()
        )

        result = detector.latest_bullish_fvg()

        self.assertTrue(
            result is None or isinstance(result, dict)
        )

    def test_latest_bearish_fvg_returns_gap_or_none(self):

        detector = FVGDetector(
            self.bearish_candles()
        )

        result = detector.latest_bearish_fvg()

        self.assertTrue(
            result is None or isinstance(result, dict)
        )

    # ==================================================
    # Counts
    # ==================================================

    def test_bullish_count_matches_result(self):

        detector = FVGDetector(
            self.bullish_candles()
        )

        self.assertEqual(
            detector.bullish_count(),
            len(detector.bullish_fvg()),
        )

    def test_bearish_count_matches_result(self):

        detector = FVGDetector(
            self.bearish_candles()
        )

        self.assertEqual(
            detector.bearish_count(),
            len(detector.bearish_fvg()),
        )


if __name__ == "__main__":
    unittest.main()
