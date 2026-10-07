import unittest

from backend.analysis_result import AnalysisResult
from backend.candle import Candle
from backend.riley_coleman_strategy import RileyColemanStrategy


class TestRileyColemanStrategy(unittest.TestCase):

    def create_analysis(self):

        analysis = AnalysisResult()

        analysis.market = "EURUSD"
        analysis.timeframe = "M5"

        return analysis

    def test_bullish_reversal_requires_bearish_trend(self):

        analysis = self.create_analysis()

        analysis.trend = "UPTREND"
        analysis.bullish_choch = True
        analysis.bullish_confirmation_candle = Candle(
            "10:30", 104, 110, 103, 109
        )

        self.assertEqual(
            RileyColemanStrategy(analysis).evaluate(),
            "WAIT",
        )

    def test_bullish_reversal_requires_choch(self):

        analysis = self.create_analysis()

        analysis.trend = "DOWNTREND"
        analysis.bullish_confirmation_candle = Candle(
            "10:30", 104, 110, 103, 109
        )

        self.assertEqual(
            RileyColemanStrategy(analysis).evaluate(),
            "WAIT",
        )

    def test_bullish_reversal_requires_confirmation(self):

        analysis = self.create_analysis()

        analysis.trend = "DOWNTREND"
        analysis.bullish_choch = True

        self.assertEqual(
            RileyColemanStrategy(analysis).evaluate(),
            "WAIT",
        )

    def test_bullish_reversal_returns_buy(self):

        analysis = self.create_analysis()

        analysis.trend = "DOWNTREND"
        analysis.bullish_choch = True
        analysis.bullish_confirmation_candle = Candle(
            "10:30", 104, 110, 103, 109
        )

        self.assertEqual(
            RileyColemanStrategy(analysis).evaluate(),
            "BUY",
        )

    def test_bearish_reversal_returns_sell(self):

        analysis = self.create_analysis()

        analysis.trend = "UPTREND"
        analysis.bearish_choch = True
        analysis.bearish_confirmation_candle = Candle(
            "10:30", 106, 108, 100, 101
        )

        self.assertEqual(
            RileyColemanStrategy(analysis).evaluate(),
            "SELL",
        )

    def test_no_reversal_returns_wait(self):

        analysis = self.create_analysis()

        analysis.trend = "SIDEWAYS"

        self.assertEqual(
            RileyColemanStrategy(analysis).evaluate(),
            "WAIT",
        )

    def test_engulfing_list_alone_does_not_create_signal(self):

        analysis = self.create_analysis()

        analysis.trend = "DOWNTREND"
        analysis.bullish_choch = True
        analysis.bullish_engulfing = [object()]

        self.assertEqual(
            RileyColemanStrategy(analysis).evaluate(),
            "WAIT",
        )


if __name__ == "__main__":
    unittest.main()
