import unittest

from backend.validation.market_validator import MarketValidator


class Candle:
    def __init__(
        self,
        time,
        open_,
        high,
        low,
        close,
    ):
        self.time = time
        self.open = open_
        self.high = high
        self.low = low
        self.close = close


class TestMarketValidator(unittest.TestCase):

    def setUp(self):

        self.validator = MarketValidator()

    # ==================================================
    # VALID DATA
    # ==================================================

    def test_valid_market_data(self):

        candles = [

            Candle(
                "10:00",
                100,
                110,
                95,
                105,
            ),

            Candle(
                "10:05",
                105,
                115,
                100,
                112,
            ),

            Candle(
                "10:10",
                112,
                118,
                110,
                117,
            ),

        ]

        valid, message = self.validator.validate(
            candles,
            "M5",
        )

        self.assertTrue(valid)
        self.assertEqual(
            message,
            "Market data validation passed.",
        )

    # ==================================================
    # DUPLICATE TIME
    # ==================================================

    def test_duplicate_candles(self):

        candles = [

            Candle(
                "10:00",
                100,
                110,
                95,
                105,
            ),

            Candle(
                "10:00",
                105,
                115,
                100,
                112,
            ),

            Candle(
                "10:10",
                112,
                118,
                110,
                117,
            ),

        ]

        valid, message = self.validator.validate(
            candles,
            "M5",
        )

        self.assertFalse(valid)

    # ==================================================
    # INVALID PRICES
    # ==================================================

    def test_invalid_prices(self):

        candles = [

            Candle(
                "10:00",
                100,
                90,
                95,
                105,
            ),

            Candle(
                "10:05",
                105,
                115,
                100,
                112,
            ),

            Candle(
                "10:10",
                112,
                118,
                110,
                117,
            ),

        ]

        valid, message = self.validator.validate(
            candles,
            "M5",
        )

        self.assertFalse(valid)

    # ==================================================
    # BAD TIMEFRAME
    # ==================================================

    def test_invalid_timeframe(self):

        candles = [

            Candle(
                "10:00",
                100,
                110,
                95,
                105,
            ),

            Candle(
                "10:03",
                105,
                115,
                100,
                112,
            ),

            Candle(
                "10:10",
                112,
                118,
                110,
                117,
            ),

        ]

        valid, message = self.validator.validate(
            candles,
            "M5",
        )

        self.assertFalse(valid)


if __name__ == "__main__":
    unittest.main()