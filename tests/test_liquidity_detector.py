import unittest

from backend.candle import Candle
from backend.liquidity_detector import LiquidityDetector


class TestLiquidityDetector(unittest.TestCase):

    def candles(self):

        return [
            Candle("09:00", 100, 105, 98, 102),
            Candle("10:00", 102, 110, 100, 108),
            Candle("11:00", 108, 110, 95, 97),
            Candle("12:00", 97, 103, 90, 101),
            Candle("13:00", 101, 115, 99, 112),
            Candle("14:00", 112, 115, 92, 95),
            Candle("15:00", 95, 100, 88, 98),
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
            LiquidityDetector(candles)

    # ==================================================
    # Buy-side liquidity
    # ==================================================

    def test_buy_side_liquidity_returns_list(self):

        detector = LiquidityDetector(
            self.candles()
        )

        result = detector.buy_side_liquidity()

        self.assertIsInstance(result, list)

    def test_buy_side_liquidity_contains_candles(self):

        detector = LiquidityDetector(
            self.candles()
        )

        result = detector.buy_side_liquidity()

        for candle in result:
            self.assertIsInstance(
                candle,
                Candle,
            )

    # ==================================================
    # Sell-side liquidity
    # ==================================================

    def test_sell_side_liquidity_returns_list(self):

        detector = LiquidityDetector(
            self.candles()
        )

        result = detector.sell_side_liquidity()

        self.assertIsInstance(result, list)

    def test_sell_side_liquidity_contains_candles(self):

        detector = LiquidityDetector(
            self.candles()
        )

        result = detector.sell_side_liquidity()

        for candle in result:
            self.assertIsInstance(
                candle,
                Candle,
            )

    # ==================================================
    # Latest liquidity
    # ==================================================

    def test_latest_buy_side_matches_last_detected_level(self):

        detector = LiquidityDetector(
            self.candles()
        )

        liquidity = detector.buy_side_liquidity()
        latest = detector.latest_buy_side()

        if liquidity:
            self.assertIs(
                latest,
                liquidity[-1],
            )
        else:
            self.assertIsNone(latest)

    def test_latest_sell_side_matches_last_detected_level(self):

        detector = LiquidityDetector(
            self.candles()
        )

        liquidity = detector.sell_side_liquidity()
        latest = detector.latest_sell_side()

        if liquidity:
            self.assertIs(
                latest,
                liquidity[-1],
            )
        else:
            self.assertIsNone(latest)

    # ==================================================
    # Liquidity prices
    # ==================================================

    def test_buy_side_prices_match_highs(self):

        detector = LiquidityDetector(
            self.candles()
        )

        liquidity = detector.buy_side_liquidity()

        expected = [
            candle.high
            for candle in liquidity
        ]

        self.assertEqual(
            detector.buy_side_prices(),
            expected,
        )

    def test_sell_side_prices_match_lows(self):

        detector = LiquidityDetector(
            self.candles()
        )

        liquidity = detector.sell_side_liquidity()

        expected = [
            candle.low
            for candle in liquidity
        ]

        self.assertEqual(
            detector.sell_side_prices(),
            expected,
        )

    # ==================================================
    # Counts
    # ==================================================

    def test_buy_side_count_matches_result(self):

        detector = LiquidityDetector(
            self.candles()
        )

        self.assertEqual(
            detector.buy_side_count(),
            len(detector.buy_side_liquidity()),
        )

    def test_sell_side_count_matches_result(self):

        detector = LiquidityDetector(
            self.candles()
        )

        self.assertEqual(
            detector.sell_side_count(),
            len(detector.sell_side_liquidity()),
        )

    def test_total_liquidity_matches_both_sides(self):

        detector = LiquidityDetector(
            self.candles()
        )

        expected = (
            detector.buy_side_count()
            + detector.sell_side_count()
        )

        self.assertEqual(
            detector.total_liquidity(),
            expected,
        )

    # ==================================================
    # Availability
    # ==================================================

    def test_has_buy_side_returns_boolean(self):

        detector = LiquidityDetector(
            self.candles()
        )

        self.assertIsInstance(
            detector.has_buy_side(),
            bool,
        )

    def test_has_sell_side_returns_boolean(self):

        detector = LiquidityDetector(
            self.candles()
        )

        self.assertIsInstance(
            detector.has_sell_side(),
            bool,
        )


if __name__ == "__main__":
    unittest.main()
