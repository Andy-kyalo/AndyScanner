import unittest

from backend.analysis_result import AnalysisResult
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
        market="US30",
        timeframe="M5",
    ):

        analysis = AnalysisResult()

        analysis.market = market
        analysis.timeframe = timeframe
        analysis.trend = trend

        engine = SignalEngine(analysis)

        # Isolate SignalEngine decision logic from
        # ConfidenceEngine scoring logic.
        engine.confidence = MockConfidence(
            confidence
        )

        return engine

    # ==================================================
    # WAIT
    # ==================================================

    def test_sideways_market_returns_wait(self):

        engine = self.create_engine(
            "SIDEWAYS",
            90,
        )

        signal = engine.generate()

        self.assertEqual(
            signal.direction,
            "WAIT",
        )

    def test_low_bullish_confidence_returns_wait(self):

        engine = self.create_engine(
            "UPTREND",
            50,
        )

        signal = engine.generate()

        self.assertEqual(
            signal.direction,
            "WAIT",
        )

    def test_low_bearish_confidence_returns_wait(self):

        engine = self.create_engine(
            "DOWNTREND",
            50,
        )

        signal = engine.generate()

        self.assertEqual(
            signal.direction,
            "WAIT",
        )

    # ==================================================
    # BUY
    # ==================================================

    def test_bullish_confidence_60_returns_buy(self):

        engine = self.create_engine(
            "UPTREND",
            60,
        )

        signal = engine.generate()

        self.assertEqual(
            signal.direction,
            "BUY",
        )

    def test_bullish_confidence_79_returns_buy(self):

        engine = self.create_engine(
            "UPTREND",
            79,
        )

        signal = engine.generate()

        self.assertEqual(
            signal.direction,
            "BUY",
        )

    # ==================================================
    # STRONG BUY
    # ==================================================

    def test_bullish_confidence_80_returns_strong_buy(self):

        engine = self.create_engine(
            "UPTREND",
            80,
        )

        signal = engine.generate()

        self.assertEqual(
            signal.direction,
            "STRONG BUY",
        )

    def test_bullish_confidence_100_returns_strong_buy(self):

        engine = self.create_engine(
            "UPTREND",
            100,
        )

        signal = engine.generate()

        self.assertEqual(
            signal.direction,
            "STRONG BUY",
        )

    # ==================================================
    # SELL
    # ==================================================

    def test_bearish_confidence_60_returns_sell(self):

        engine = self.create_engine(
            "DOWNTREND",
            60,
        )

        signal = engine.generate()

        self.assertEqual(
            signal.direction,
            "SELL",
        )

    def test_bearish_confidence_79_returns_sell(self):

        engine = self.create_engine(
            "DOWNTREND",
            79,
        )

        signal = engine.generate()

        self.assertEqual(
            signal.direction,
            "SELL",
        )

    # ==================================================
    # STRONG SELL
    # ==================================================

    def test_bearish_confidence_80_returns_strong_sell(self):

        engine = self.create_engine(
            "DOWNTREND",
            80,
        )

        signal = engine.generate()

        self.assertEqual(
            signal.direction,
            "STRONG SELL",
        )

    def test_bearish_confidence_100_returns_strong_sell(self):

        engine = self.create_engine(
            "DOWNTREND",
            100,
        )

        signal = engine.generate()

        self.assertEqual(
            signal.direction,
            "STRONG SELL",
        )

    # ==================================================
    # SIGNAL DATA
    # ==================================================

    def test_signal_contains_confidence(self):

        engine = self.create_engine(
            "UPTREND",
            80,
        )

        signal = engine.generate()

        self.assertEqual(
            signal.confidence,
            80,
        )

    def test_signal_contains_default_timeframe(self):

        engine = self.create_engine(
            "UPTREND",
            80,
        )

        signal = engine.generate()

        self.assertEqual(
            signal.timeframe,
            "M5",
        )

    def test_signal_preserves_analysis_market_and_timeframe(self):

        engine = self.create_engine(
            "UPTREND",
            80,
            market="NAS100",
            timeframe="M15",
        )

        signal = engine.generate()

        self.assertEqual(
            signal.market,
            "NAS100",
        )

        self.assertEqual(
            signal.timeframe,
            "M15",
        )

    # ==================================================
    # REAL CONFIDENCE ENGINE INTEGRATION
    # ==================================================

    def test_real_bullish_analysis_produces_strong_buy(self):

        analysis = AnalysisResult()

        analysis.market = "US30"
        analysis.timeframe = "M5"
        analysis.trend = "UPTREND"

        analysis.bullish_bos = True
        analysis.bullish_choch = True
        analysis.bullish_order_block = object()
        analysis.bullish_fvg = [object()]
        analysis.buy_side_liquidity = [object()]
        analysis.bullish_engulfing = [object()]

        signal = SignalEngine(analysis).generate()

        self.assertEqual(
            signal.direction,
            "STRONG BUY",
        )

        self.assertEqual(
            signal.confidence,
            100,
        )

    def test_real_bearish_analysis_produces_strong_sell(self):

        analysis = AnalysisResult()

        analysis.market = "US30"
        analysis.timeframe = "M5"
        analysis.trend = "DOWNTREND"

        analysis.bearish_bos = True
        analysis.bearish_choch = True
        analysis.bearish_order_block = object()
        analysis.bearish_fvg = [object()]
        analysis.sell_side_liquidity = [object()]
        analysis.bearish_engulfing = [object()]

        signal = SignalEngine(analysis).generate()

        self.assertEqual(
            signal.direction,
            "STRONG SELL",
        )

        self.assertEqual(
            signal.confidence,
            100,
        )

    def test_real_weak_analysis_produces_wait(self):

        analysis = AnalysisResult()

        analysis.market = "US30"
        analysis.timeframe = "M5"
        analysis.trend = "UPTREND"

        signal = SignalEngine(analysis).generate()

        self.assertEqual(
            signal.direction,
            "WAIT",
        )

        self.assertEqual(
            signal.confidence,
            5,
        )


if __name__ == "__main__":
    unittest.main()
