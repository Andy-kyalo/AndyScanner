import unittest

from datetime import datetime, timezone, timedelta

from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.stages.analysis_stage import AnalysisStage


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


class TestAnalysisStage(unittest.TestCase):

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
                105,
                100,
                103,
            ),
            Candle(
                "10:05",
                103,
                110,
                102,
                108,
            ),
            Candle(
                "10:10",
                108,
                109,
                95,
                98,
            ),
            Candle(
                "10:15",
                98,
                108,
                97,
                106,
            ),
            Candle(
                "10:20",
                106,
                115,
                105,
                113,
            ),
            Candle(
                "10:25",
                113,
                114,
                102,
                106,
            ),
            Candle(
                "10:30",
                106,
                116,
                105,
                114,
            ),
            Candle(
                "10:35",
                114,
                120,
                112,
                118,
            ),
        ]

        return context

    # ==================================================
    # ANALYSIS STAGE
    # ==================================================

    def test_analysis_stage_creates_analysis_result(self):
        context = self.create_context()

        stage = AnalysisStage()
        result = stage.run(context)

        self.assertIs(result, context)
        self.assertIsNotNone(context.analyzer)
        self.assertIsNotNone(context.analysis)

    # ==================================================
    # MARKET INFORMATION
    # ==================================================

    def test_analysis_contains_market_information(self):
        context = self.create_context()

        AnalysisStage().run(context)

        analysis = context.analysis

        self.assertEqual(
            analysis.market,
            "US30",
        )

        self.assertEqual(
            analysis.timeframe,
            "M5",
        )

    # ==================================================
    # TREND
    # ==================================================

    def test_analysis_contains_trend(self):
        context = self.create_context()

        AnalysisStage().run(context)

        analysis = context.analysis

        self.assertEqual(
            analysis.trend,
            "UPTREND",
        )

        self.assertEqual(
            context.trend,
            "UPTREND",
        )

        self.assertEqual(
            context.get_metadata("trend"),
            "UPTREND",
        )

    # ==================================================
    # PRICE STATISTICS
    # ==================================================

    def test_analysis_contains_price_statistics(self):
        context = self.create_context()

        AnalysisStage().run(context)

        analysis = context.analysis

        self.assertEqual(
            analysis.highest_high,
            120,
        )

        self.assertEqual(
            analysis.lowest_low,
            95,
        )

        self.assertIsNotNone(
            analysis.strongest_candle,
        )

    # ==================================================
    # STRUCTURE
    # ==================================================

    def test_analysis_contains_structure_flags(self):
        context = self.create_context()

        AnalysisStage().run(context)

        analysis = context.analysis

        self.assertTrue(
            analysis.bullish_bos,
        )

        self.assertFalse(
            analysis.bearish_bos,
        )

        self.assertFalse(
            analysis.bullish_choch,
        )

        self.assertFalse(
            analysis.bearish_choch,
        )

    # ==================================================
    # METADATA
    # ==================================================

    def test_analysis_metadata(self):
        context = self.create_context()

        AnalysisStage().run(context)

        self.assertEqual(
            context.get_metadata("structure"),
            context.analysis.structure,
        )

        self.assertEqual(
            context.get_metadata("bullish_fvg_count"),
            context.analysis.bullish_fvg_count,
        )

        self.assertEqual(
            context.get_metadata("bearish_fvg_count"),
            context.analysis.bearish_fvg_count,
        )

        self.assertEqual(
            context.get_metadata("buy_side_count"),
            context.analysis.buy_side_count,
        )

        self.assertEqual(
            context.get_metadata("sell_side_count"),
            context.analysis.sell_side_count,
        )

    # ==================================================
    # RECALCULATION
    # ==================================================

    def test_analysis_is_recalculated_for_each_scan(self):
        first_context = self.create_context()
        second_context = self.create_context()

        second_context.candles = [
            Candle(
                "10:00",
                200,
                210,
                195,
                205,
            ),
            Candle(
                "10:05",
                205,
                215,
                200,
                212,
            ),
            Candle(
                "10:10",
                212,
                218,
                210,
                217,
            ),
        ]

        AnalysisStage().run(first_context)
        AnalysisStage().run(second_context)

        self.assertIsNot(
            first_context.analysis,
            second_context.analysis,
        )

        self.assertIsNot(
            first_context.analyzer,
            second_context.analyzer,
        )

        self.assertEqual(
            first_context.analysis.highest_high,
            120,
        )

        self.assertEqual(
            second_context.analysis.highest_high,
            218,
        )

        self.assertEqual(
            first_context.analysis.lowest_low,
            95,
        )

        self.assertEqual(
            second_context.analysis.lowest_low,
            195,
        )

    # ==================================================
    # CONFIRMATION CANDLE COMPLETION
    # ==================================================

    def create_completion_fixture(self):
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

        context.candles = [
            Candle(
                (
                    base + timedelta(minutes=i * 5)
                ).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                100,
                101,
                99,
                100,
            )
            for i in range(12)
        ]

        # Structural reversal fixture.

        context.candles[1] = Candle(
            (
                base + timedelta(minutes=5)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            100,
            106,
            99,
            104,
        )

        context.candles[2] = Candle(
            (
                base + timedelta(minutes=10)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            104,
            105,
            97,
            99,
        )

        context.candles[3] = Candle(
            (
                base + timedelta(minutes=15)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            99,
            102,
            98,
            101,
        )

        context.candles[4] = Candle(
            (
                base + timedelta(minutes=20)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            101,
            102,
            94,
            95,
        )

        context.candles[5] = Candle(
            (
                base + timedelta(minutes=25)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            95,
            103,
            94,
            102,
        )

        context.candles[6] = Candle(
            (
                base + timedelta(minutes=30)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            102,
            104,
            98,
            99,
        )

        context.candles[7] = Candle(
            (
                base + timedelta(minutes=35)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            98,
            108,
            98,
            107,
        )

        context.candles[8] = Candle(
            (
                base + timedelta(minutes=40)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            107,
            109,
            105,
            108,
        )

        # Protected HL.
        context.candles[9] = Candle(
            (
                base + timedelta(minutes=45)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            108,
            109,
            103,
            104,
        )

        # Candle immediately before confirmation.
        context.candles[10] = Candle(
            (
                base + timedelta(minutes=50)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            107,
            108,
            104,
            104,
        )

        # Bullish confirmation candle.
        context.candles[11] = Candle(
            (
                base + timedelta(minutes=55)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            103,
            110,
            102,
            109,
        )

        return context, base

    def create_bearish_completion_fixture(self):
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

        context.candles = [
            Candle(
                (
                    base + timedelta(minutes=i * 5)
                ).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                100,
                101,
                99,
                100,
            )
            for i in range(12)
        ]

        # Initial structure.
        context.candles[1] = Candle(
            (
                base + timedelta(minutes=5)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            100,
            104,
            99,
            103,
        )

        # Initial swing low.
        context.candles[2] = Candle(
            (
                base + timedelta(minutes=10)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            103,
            105,
            96,
            97,
        )

        # Higher high.
        context.candles[3] = Candle(
            (
                base + timedelta(minutes=15)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            97,
            106,
            95,
            105,
        )

        # Higher low.
        context.candles[4] = Candle(
            (
                base + timedelta(minutes=20)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            105,
            107,
            99,
            100,
        )

        # Bullish break above HH.
        context.candles[5] = Candle(
            (
                base + timedelta(minutes=25)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            100,
            108,
            98,
            107,
        )

        # Higher high.
        context.candles[6] = Candle(
            (
                base + timedelta(minutes=30)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            107,
            110,
            104,
            105,
        )

        # Bearish CHOCH: close below protected HL.
        context.candles[7] = Candle(
            (
                base + timedelta(minutes=35)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            105,
            106,
            97,
            98,
        )

        # Recovery candle.
        context.candles[8] = Candle(
            (
                base + timedelta(minutes=40)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            98,
            100,
            93,
            99,
        )

        # Protected LH.
        context.candles[9] = Candle(
            (
                base + timedelta(minutes=45)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            99,
            101,
            92,
            94,
        )

        # Bullish candle immediately before confirmation.
        context.candles[10] = Candle(
            (
                base + timedelta(minutes=50)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            94,
            98,
            93,
            96,
        )

        # Bearish engulfing confirmation candle.
        context.candles[11] = Candle(
            (
                base + timedelta(minutes=55)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            97,
            99,
            91,
            92,
        )

        return context, base

    def test_confirmation_candle_is_rejected_before_timeframe_completion(self):
        context, base = self.create_completion_fixture()

        context.set_metadata(
            "now",
            base + timedelta(minutes=59),
        )

        AnalysisStage().run(context)

        self.assertIsNone(
            context.analysis.bullish_confirmation_candle
        )

    def test_confirmation_candle_is_accepted_after_timeframe_completion(self):
        context, base = self.create_completion_fixture()

        context.set_metadata(
            "now",
            base + timedelta(minutes=60),
        )

        AnalysisStage().run(context)

        self.assertIsNotNone(
            context.analysis.bullish_confirmation_candle
        )

        confirmation_index = context.candles.index(
            context.analysis.bullish_confirmation_candle
        )

        self.assertEqual(
            confirmation_index,
            11,
        )

        self.assertIsNotNone(
            context.analysis.protected_low
        )

        self.assertEqual(
            context.analysis.protected_low.label,
            "HL",
        )

        self.assertEqual(
            context.analysis.protected_low.index,
            9,
        )

        self.assertGreater(
            confirmation_index,
            context.analysis.protected_low.index,
        )

    def test_bearish_confirmation_candle_is_rejected_before_timeframe_completion(
        self,
    ):
        context, base = self.create_bearish_completion_fixture()

        context.set_metadata(
            "now",
            base + timedelta(minutes=59),
        )

        AnalysisStage().run(context)

        self.assertIsNone(
            context.analysis.bearish_confirmation_candle
        )

    def test_bearish_confirmation_candle_is_accepted_after_timeframe_completion(
        self,
    ):
        context, base = self.create_bearish_completion_fixture()

        context.set_metadata(
            "now",
            base + timedelta(minutes=60),
        )

        AnalysisStage().run(context)

        self.assertIsNotNone(
            context.analysis.bearish_confirmation_candle
        )

        confirmation_index = context.candles.index(
            context.analysis.bearish_confirmation_candle
        )

        self.assertEqual(
            confirmation_index,
            11,
        )

        self.assertIsNotNone(
            context.analysis.protected_high
        )

        self.assertEqual(
            context.analysis.protected_high.label,
            "LH",
        )

        self.assertEqual(
            context.analysis.protected_high.index,
            9,
        )

        self.assertGreater(
            confirmation_index,
            context.analysis.protected_high.index,
        )


if __name__ == "__main__":
    unittest.main()