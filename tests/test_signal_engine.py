import unittest

from backend.analysis_result import AnalysisResult
from backend.candle import Candle
from backend.signal_engine import SignalEngine


class MockConfidence:
    def __init__(self, score):
        self.score = score

    def calculate(self):
        return self.score


class TestSignalEngine(unittest.TestCase):

    def create_engine(
        self,
        trend,
        confidence,
        bullish_choch=False,
        bearish_choch=False,
        bullish_engulfing=False,
        bearish_engulfing=False,
        market="US30",
        timeframe="M5",
    ):
        analysis = AnalysisResult()

        analysis.market = market
        analysis.timeframe = timeframe
        analysis.trend = trend

        analysis.bullish_choch = bullish_choch
        analysis.bearish_choch = bearish_choch

        analysis.bullish_engulfing = (
            [object()] if bullish_engulfing else []
        )
        analysis.bearish_engulfing = (
            [object()] if bearish_engulfing else []
        )

        analysis.bullish_confirmation_candle = (
            Candle("10:30", 104, 110, 103, 109)
            if bullish_engulfing else None
        )
        analysis.bearish_confirmation_candle = (
            Candle("10:30", 106, 108, 100, 101)
            if bearish_engulfing else None
        )

        engine = SignalEngine(analysis)
        engine.confidence = MockConfidence(confidence)

        return engine

    # ==================================================
    # RILEY BUY
    # ==================================================

    def test_bullish_reversal_returns_buy(self):
        engine = self.create_engine(
            "DOWNTREND",
            60,
            bullish_choch=True,
            bullish_engulfing=True,
        )

        signal = engine.generate()

        self.assertEqual(signal.direction, "BUY")
        self.assertEqual(signal.confidence, 60)

    def test_bullish_reversal_returns_buy_at_high_confidence(self):
        engine = self.create_engine(
            "DOWNTREND",
            100,
            bullish_choch=True,
            bullish_engulfing=True,
        )

        signal = engine.generate()

        self.assertEqual(signal.direction, "BUY")
        self.assertEqual(signal.confidence, 100)

    def test_bullish_reversal_does_not_require_high_confidence(self):
        engine = self.create_engine(
            "DOWNTREND",
            20,
            bullish_choch=True,
            bullish_engulfing=True,
        )

        signal = engine.generate()

        self.assertEqual(signal.direction, "BUY")
        self.assertEqual(signal.confidence, 20)

    # ==================================================
    # RILEY SELL
    # ==================================================

    def test_bearish_reversal_returns_sell(self):
        engine = self.create_engine(
            "UPTREND",
            60,
            bearish_choch=True,
            bearish_engulfing=True,
        )

        signal = engine.generate()

        self.assertEqual(signal.direction, "SELL")
        self.assertEqual(signal.confidence, 60)

    def test_bearish_reversal_returns_sell_at_high_confidence(self):
        engine = self.create_engine(
            "UPTREND",
            100,
            bearish_choch=True,
            bearish_engulfing=True,
        )

        signal = engine.generate()

        self.assertEqual(signal.direction, "SELL")
        self.assertEqual(signal.confidence, 100)

    def test_bearish_reversal_does_not_require_high_confidence(self):
        engine = self.create_engine(
            "UPTREND",
            20,
            bearish_choch=True,
            bearish_engulfing=True,
        )

        signal = engine.generate()

        self.assertEqual(signal.direction, "SELL")
        self.assertEqual(signal.confidence, 20)

    # ==================================================
    # RILEY WAIT
    # ==================================================

    def test_sideways_market_returns_wait(self):
        engine = self.create_engine(
            "SIDEWAYS",
            100,
            bullish_choch=True,
            bullish_engulfing=True,
            bearish_choch=True,
            bearish_engulfing=True,
        )

        signal = engine.generate()

        self.assertEqual(signal.direction, "WAIT")

    def test_uptrend_without_bearish_reversal_returns_wait(self):
        engine = self.create_engine(
            "UPTREND",
            100,
            bullish_choch=True,
            bullish_engulfing=True,
        )

        signal = engine.generate()

        self.assertEqual(signal.direction, "WAIT")

    def test_downtrend_without_bullish_reversal_returns_wait(self):
        engine = self.create_engine(
            "DOWNTREND",
            100,
            bearish_choch=True,
            bearish_engulfing=True,
        )

        signal = engine.generate()

        self.assertEqual(signal.direction, "WAIT")

    def test_bullish_choch_without_confirmation_returns_wait(self):
        engine = self.create_engine(
            "DOWNTREND",
            100,
            bullish_choch=True,
        )

        signal = engine.generate()

        self.assertEqual(signal.direction, "WAIT")

    def test_bearish_choch_without_confirmation_returns_wait(self):
        engine = self.create_engine(
            "UPTREND",
            100,
            bearish_choch=True,
        )

        signal = engine.generate()

        self.assertEqual(signal.direction, "WAIT")

    # ==================================================
    # SIGNAL DATA
    # ==================================================

    def test_signal_contains_confidence(self):
        engine = self.create_engine(
            "DOWNTREND",
            80,
            bullish_choch=True,
            bullish_engulfing=True,
        )

        signal = engine.generate()

        self.assertEqual(signal.confidence, 80)

    def test_signal_contains_default_timeframe(self):
        engine = self.create_engine(
            "DOWNTREND",
            80,
            bullish_choch=True,
            bullish_engulfing=True,
        )

        signal = engine.generate()

        self.assertEqual(signal.timeframe, "M5")

    def test_signal_preserves_analysis_market_and_timeframe(self):
        engine = self.create_engine(
            "UPTREND",
            80,
            bearish_choch=True,
            bearish_engulfing=True,
            market="NAS100",
            timeframe="M15",
        )

        signal = engine.generate()

        self.assertEqual(signal.market, "NAS100")
        self.assertEqual(signal.timeframe, "M15")

    # ==================================================
    # REAL CONFIDENCE ENGINE INTEGRATION
    # ==================================================

    def test_real_bullish_reversal_produces_buy(self):
        analysis = AnalysisResult()

        analysis.market = "US30"
        analysis.timeframe = "M5"
        analysis.trend = "DOWNTREND"

        analysis.bullish_bos = True
        analysis.bullish_choch = True
        analysis.bullish_order_block = object()
        analysis.bullish_fvg = [object()]
        analysis.buy_side_liquidity = [object()]
        analysis.bullish_engulfing = [object()]
        analysis.bullish_confirmation_candle = Candle(
            "10:30", 104, 110, 103, 109
        )

        signal = SignalEngine(analysis).generate()

        self.assertEqual(signal.direction, "BUY")
        self.assertEqual(signal.confidence, 5)

    def test_real_bearish_reversal_produces_sell(self):
        analysis = AnalysisResult()

        analysis.market = "US30"
        analysis.timeframe = "M5"
        analysis.trend = "UPTREND"

        analysis.bearish_bos = True
        analysis.bearish_choch = True
        analysis.bearish_order_block = object()
        analysis.bearish_fvg = [object()]
        analysis.sell_side_liquidity = [object()]
        analysis.bearish_engulfing = [object()]
        analysis.bearish_confirmation_candle = Candle(
            "10:30", 106, 108, 100, 101
        )

        signal = SignalEngine(analysis).generate()

        self.assertEqual(signal.direction, "SELL")
        self.assertEqual(signal.confidence, 5)

    def test_real_weak_analysis_produces_wait(self):
        analysis = AnalysisResult()

        analysis.market = "US30"
        analysis.timeframe = "M5"
        analysis.trend = "UPTREND"

        signal = SignalEngine(analysis).generate()

        self.assertEqual(signal.direction, "WAIT")
        self.assertEqual(signal.confidence, 5)


if __name__ == "__main__":
    unittest.main()
