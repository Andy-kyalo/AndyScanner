import unittest

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

        return context

    # ==================================================
    # ANALYSIS STAGE
    # ==================================================

    def test_analysis_stage_creates_analysis_result(self):

        context = self.create_context()

        stage = AnalysisStage()

        result = stage.run(context)

        self.assertIs(result, context)

        self.assertIsNotNone(
            context.analyzer
        )

        self.assertIsNotNone(
            context.analysis
        )

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
            118,
        )

        self.assertEqual(
            analysis.lowest_low,
            95,
        )

        self.assertIsNotNone(
            analysis.strongest_candle
        )

    # ==================================================
    # STRUCTURE
    # ==================================================

    def test_analysis_contains_structure_flags(self):

        context = self.create_context()

        AnalysisStage().run(context)

        analysis = context.analysis

        self.assertFalse(
            analysis.bullish_bos
        )

        self.assertFalse(
            analysis.bearish_bos
        )

        self.assertFalse(
            analysis.bullish_choch
        )

        self.assertFalse(
            analysis.bearish_choch
        )

    # ==================================================
    # METADATA
    # ==================================================

    def test_analysis_metadata(self):

        context = self.create_context()

        AnalysisStage().run(context)

        self.assertEqual(
            context.get_metadata("structure"),
            "NO_STRUCTURE",
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
            118,
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


if __name__ == "__main__":
    unittest.main()
