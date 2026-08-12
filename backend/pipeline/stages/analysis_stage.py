"""
analysis_stage.py

Analysis Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_stage import PipelineStage
from backend.analyzer import Analyzer
from backend.analysis_result import AnalysisResult


class AnalysisStage(PipelineStage):
    """
    Performs market analysis and produces
    a structured AnalysisResult.
    """

    def __init__(self):

        super().__init__("Analysis Stage")

    def execute(self, context):

        analyzer = Analyzer(
            context.candles
        )

        result = AnalysisResult()

        result.market = context.market
        result.timeframe = context.timeframe

        # ==========================================
        # MARKET STATISTICS
        # ==========================================

        result.trend = analyzer.trend()

        result.highest_high = analyzer.highest_high()

        result.lowest_low = analyzer.lowest_low()

        result.strongest_candle = analyzer.strongest_candle()

        # ==========================================
        # MARKET STRUCTURE
        # ==========================================

        result.bullish_bos = analyzer.bullish_bos()

        result.bearish_bos = analyzer.bearish_bos()

        result.bullish_choch = analyzer.bullish_choch()

        result.bearish_choch = analyzer.bearish_choch()

        # ==========================================
        # PRICE ACTION
        # ==========================================

        result.bullish_engulfing = (
            analyzer.bullish_engulfing()
        )

        result.bearish_engulfing = (
            analyzer.bearish_engulfing()
        )

        # ==========================================
        # FAIR VALUE GAPS
        # ==========================================

        result.bullish_fvg = (
            analyzer.bullish_fvg()
        )

        result.bearish_fvg = (
            analyzer.bearish_fvg()
        )

        # ==========================================
        # LIQUIDITY
        # ==========================================

        result.buy_side_liquidity = (
            analyzer.buy_side_liquidity()
        )

        result.sell_side_liquidity = (
            analyzer.sell_side_liquidity()
        )

        # ==========================================
        # ORDER BLOCKS
        # ==========================================

        result.bullish_order_block = (
            analyzer.bullish_order_block()
        )

        result.bearish_order_block = (
            analyzer.bearish_order_block()
        )

        # ==========================================
        # CONTEXT
        # ==========================================

        context.analyzer = analyzer

        context.analysis = result

        # Keep the existing context.trend
        # for backwards compatibility.
        context.trend = result.trend

        # ==========================================
        # METADATA
        # ==========================================

        context.set_metadata(
            "trend",
            result.trend,
        )
        context.set_metadata(
            "structure",
            result.structure,
        )
        context.set_metadata(
            "bullish_bos",
            result.bullish_bos,
        )
        context.set_metadata(
            "bearish_bos",
            result.bearish_bos,
        )
        context.set_metadata(
            "bullish_choch",
            result.bullish_choch,
        )
        context.set_metadata(
            "bearish_choch",
            result.bearish_choch,
        )
        context.set_metadata(
            "bullish_fvg_count",
            result.bullish_fvg_count,
        )
        context.set_metadata(
            "bearish_fvg_count",
            result.bearish_fvg_count,
        )
        context.set_metadata(
            "buy_side_count",
            result.buy_side_count,
        )
        context.set_metadata(
            "sell_side_count",
            result.sell_side_count,
        )
        return context
