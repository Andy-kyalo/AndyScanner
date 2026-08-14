import unittest

from backend.candle import Candle
from backend.order_block_detector import OrderBlockDetector


class TestOrderBlockDetector(unittest.TestCase):

    def bullish_candles(self):

        return [
            Candle("09:00", 100, 102, 99, 101),
            Candle("10:00", 101, 103, 100, 102),
            Candle("11:00", 102, 104, 101, 103),
            Candle("12:00", 103, 110, 102, 109),
        ]

    def bearish_candles(self):

        return [
            Candle("09:00", 110, 111, 108, 109),
            Candle("10:00", 109, 110, 106, 107),
            Candle("11:00", 107, 108, 104, 105),
            Candle("12:00", 105, 106, 99, 100),
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
            OrderBlockDetector(candles)

    # ==================================================
    # Bullish Order Block
    # ==================================================

    def test_bullish_order_block_returns_candle_or_none(self):

        detector = OrderBlockDetector(
            self.bullish_candles()
        )

        result = detector.bullish_order_block()

        self.assertTrue(
            result is None or isinstance(result, Candle)
        )

    # ==================================================
    # Bearish Order Block
    # ==================================================

    def test_bearish_order_block_returns_candle_or_none(self):

        detector = OrderBlockDetector(
            self.bearish_candles()
        )

        result = detector.bearish_order_block()

        self.assertTrue(
            result is None or isinstance(result, Candle)
        )

    # ==================================================
    # Availability
    # ==================================================

    def test_has_bullish_order_block_returns_boolean(self):

        detector = OrderBlockDetector(
            self.bullish_candles()
        )

        self.assertIsInstance(
            detector.has_bullish_order_block(),
            bool,
        )

    def test_has_bearish_order_block_returns_boolean(self):

        detector = OrderBlockDetector(
            self.bearish_candles()
        )

        self.assertIsInstance(
            detector.has_bearish_order_block(),
            bool,
        )

    # ==================================================
    # Levels
    # ==================================================

    def test_bullish_order_block_levels_are_consistent(self):

        detector = OrderBlockDetector(
            self.bullish_candles()
        )

        block = detector.bullish_order_block()

        if block is not None:

            self.assertEqual(
                detector.bullish_order_block_high(),
                block.high,
            )

            self.assertEqual(
                detector.bullish_order_block_low(),
                block.low,
            )

    def test_bearish_order_block_levels_are_consistent(self):

        detector = OrderBlockDetector(
            self.bearish_candles()
        )

        block = detector.bearish_order_block()

        if block is not None:

            self.assertEqual(
                detector.bearish_order_block_high(),
                block.high,
            )

            self.assertEqual(
                detector.bearish_order_block_low(),
                block.low,
            )


if __name__ == "__main__":
    unittest.main()
