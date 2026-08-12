import unittest

from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.stages.analysis_stage import AnalysisStage
from backend.pipeline.stages.signal_stage import SignalStage


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

    def is_bullish(self):
        return self.close > self.open

    def is_bearish(self):
        return self.close < self.open

    def body_size(self):
        return abs(self.close - self.open)


class TestSignalStage(unittest.TestCase):

    def create_context(self):

        context = PipelineContext()

        context.start(
            "US30",
            "M5",
        )

        context.candles = [
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

        # Analysis Stage must run first because
        # Signal Stage depends on context.analyzer.

        AnalysisStage().run(context)

        return context

    # ==================================================
    # SIGNAL STAGE
    # ==================================================

    def test_signal_stage_returns_context(self):

        context = self.create_context()

        result = SignalStage().run(context)

        self.assertIs(
            result,
            context,
        )

    # ==================================================
    # SIGNAL CREATION
    # ==================================================

    def test_signal_stage_creates_signal(self):

        context = self.create_context()

        SignalStage().run(context)

        self.assertIsNotNone(
            context.signal
        )

    # ==================================================
    # SIGNAL MARKET
    # ==================================================

    def test_signal_contains_market(self):

        context = self.create_context()

        SignalStage().run(context)

        self.assertEqual(
            context.signal.market,
            "US30",
        )

    # ==================================================
    # SIGNAL TIMEFRAME
    # ==================================================

    def test_signal_contains_timeframe(self):

        context = self.create_context()

        SignalStage().run(context)

        self.assertEqual(
            context.signal.timeframe,
            "M5",
        )

    # ==================================================
    # SIGNAL DIRECTION
    # ==================================================

    def test_signal_direction_is_valid(self):

        context = self.create_context()

        SignalStage().run(context)

        self.assertIn(
            context.signal.direction,
            (
                "WAIT",
                "BUY",
                "STRONG BUY",
                "SELL",
                "STRONG SELL",
            ),
        )

    # ==================================================
    # CONFIDENCE
    # ==================================================

    def test_signal_confidence_is_valid(self):

        context = self.create_context()

        SignalStage().run(context)

        self.assertGreaterEqual(
            context.signal.confidence,
            0,
        )

        self.assertLessEqual(
            context.signal.confidence,
            100,
        )

    # ==================================================
    # METADATA
    # ==================================================

    def test_signal_metadata(self):

        context = self.create_context()

        SignalStage().run(context)

        self.assertEqual(
            context.get_metadata("signal"),
            context.signal.direction,
        )

        self.assertEqual(
            context.get_metadata("confidence"),
            context.signal.confidence,
        )


if __name__ == "__main__":
    unittest.main()
