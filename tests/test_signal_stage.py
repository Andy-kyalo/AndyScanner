import unittest

from datetime import datetime, timezone, timedelta

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

    # ==================================================
    # END-TO-END RILEY INTEGRATION
    # ==================================================

    def create_bullish_reversal_context(self):

        context = PipelineContext()

        context.start(
            "US30",
            "M5",
        )

        base = datetime(
            2026,
            1,
            1,
            10,
            0,
            tzinfo=timezone.utc,
        )

        values = [
            # 0 - filler
            (100, 100, 99, 100),

            # 1 - INITIAL HIGH = 110
            (100, 110, 99, 105),

            # 2 - INITIAL LOW = 90
            (105, 102, 90, 92),

            # 3 - LH = 103
            (92, 103, 91, 100),

            # 4 - LL = 85
            (100, 101, 85, 95),

            # 5 - confirms LL pivot
            (95, 100, 86, 90),

            # 6 - bearish STRUCTURE_BREAK
            # close < active low 85
            (90, 92, 78, 80),

            # 7 - bullish CHOCH
            # close > active high 103
            (80, 112, 82, 110),

            # 8 - protected HL
            # low 80 > previous LL 78
            # bearish candle
            (110, 108, 80, 100),

            # 9 - bearish candle before confirmation
            (102, 100, 81, 98),

            # 10 - bullish engulfing confirmation
            (97, 106, 96, 105),

            # 11 - final LL
            (105, 104, 75, 80),

            # 12 - confirms final LL
            (80, 103, 76, 90),
        ]

        context.candles = [
            Candle(
                (
                    base + timedelta(minutes=i * 5)
                ).strftime("%Y-%m-%d %H:%M:%S"),
                open_,
                high,
                low,
                close,
            )
            for i, (open_, high, low, close)
            in enumerate(values)
        ]

        context.set_metadata(
            "now",
            base + timedelta(minutes=len(values) * 5),
        )

        return context

    def create_bearish_reversal_context(self):

        context = PipelineContext()

        context.start(
            "US30",
            "M5",
        )

        base = datetime(
            2026,
            1,
            1,
            10,
            0,
            tzinfo=timezone.utc,
        )

        values = [
            # 0 - filler
            (100, 100, 99, 100),

            # 1 - INITIAL HIGH = 105
            (100, 105, 99, 103),

            # 2 - INITIAL LOW = 90
            (103, 104, 90, 92),

            # 3 - HH = 110
            (92, 110, 96, 108),

            # 4 - HL = 95
            (108, 109, 95, 100),

            # 5 - confirms HL pivot
            (100, 105, 96, 102),

            # 6 - bullish BOS
            # close > active high 110
            (102, 115, 98, 112),

            # 7 - bearish CHOCH
            # close < active low 95
            (112, 100, 94, 94),

            # 8 - protected LH
            # high 105 < previous HH 115
            # bullish candle
            (94, 105, 90, 102),

            # 9 - bullish candle before confirmation
            (101, 104, 91, 103),

            # 10 - bullish candle before confirmation
            (104, 106, 90, 105),

            # 11 - final HH
            # high 118 > previous HH 115
            # close stays below active high 105
            (90, 118, 88, 100),

            # 12 - between final HH and LH
            (100, 110, 100, 105),

            # 13 - protected LH
            # high 112 remains below previous HH 118
            # bullish candle
            (105, 112, 95, 108),

            # 14 - bearish engulfing confirmation
            # previous candle 13: 105 -> 108
            # current candle: 109 -> 104
            # 109 > 108 and 104 < 105
            (109, 110, 96, 104),

            # 15 - final HH
            (105, 110, 100, 108),

            # 16 - higher final HH
            # close remains below active structural level
            (108, 120, 97, 100),

            # 17 - confirms final HH
            (100, 110, 96, 105),
        ]

        context.candles = [
            Candle(
                (
                    base + timedelta(minutes=i * 5)
                ).strftime("%Y-%m-%d %H:%M:%S"),
                open_,
                high,
                low,
                close,
            )
            for i, (open_, high, low, close)
            in enumerate(values)
        ]

        context.set_metadata(
            "now",
            base + timedelta(minutes=len(values) * 5),
        )

        return context

    # ==================================================
    # BUY INTEGRATION
    # ==================================================

    def test_analysis_to_signal_produces_buy(self):

        context = self.create_bullish_reversal_context()

        AnalysisStage().run(context)
        SignalStage().run(context)

        self.assertEqual(
            context.analysis.trend,
            "DOWNTREND",
        )

        self.assertTrue(
            context.analysis.bullish_choch
        )

        self.assertIsNotNone(
            context.analysis.protected_low
        )

        self.assertEqual(
            context.analysis.protected_low.label,
            "HL",
        )

        self.assertIsNotNone(
            context.analysis.bullish_confirmation_candle
        )

        self.assertEqual(
            context.signal.direction,
            "BUY",
        )

    # ==================================================
    # SELL INTEGRATION
    # ==================================================

    def test_analysis_to_signal_produces_sell(self):

        context = self.create_bearish_reversal_context()

        AnalysisStage().run(context)
        SignalStage().run(context)

        self.assertEqual(
            context.analysis.trend,
            "UPTREND",
        )

        self.assertTrue(
            context.analysis.bearish_choch
        )

        self.assertIsNotNone(
            context.analysis.protected_high
        )

        self.assertEqual(
            context.analysis.protected_high.label,
            "LH",
        )

        self.assertIsNotNone(
            context.analysis.bearish_confirmation_candle
        )

        self.assertEqual(
            context.signal.direction,
            "SELL",
        )

    # ==================================================
    # WAIT INTEGRATION
    # ==================================================

    def test_analysis_to_signal_produces_wait_without_reversal(self):

        context = self.create_context()

        AnalysisStage().run(context)
        SignalStage().run(context)

        self.assertEqual(
            context.signal.direction,
            "WAIT",
        )


if __name__ == "__main__":
    unittest.main()