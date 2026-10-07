"""
analysis_stage.py

Analysis Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime, timezone

from backend.pipeline.pipeline_stage import PipelineStage
from backend.analyzer import Analyzer
from backend.analysis_result import AnalysisResult


TIMEFRAME_SECONDS = {
    "M1": 60,
    "M5": 300,
    "M15": 900,
    "M30": 1800,
    "H1": 3600,
    "H4": 14400,
    "D1": 86400,
}


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

        result.structural_state = (
            analyzer.structural_state()
        )

        result.swing_highs = (
            analyzer.swing_highs()
        )

        result.swing_lows = (
            analyzer.swing_lows()
        )

        result.protected_high = (
            analyzer.protected_high()
        )

        result.protected_low = (
            analyzer.protected_low()
        )

        result.last_bos = (
            analyzer.last_bos()
        )

        result.last_choch = (
            analyzer.last_choch()
        )

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
        # CONFIRMATION-CANDLE COMPLETION
        # ==========================================

        timeframe_seconds = TIMEFRAME_SECONDS.get(
            context.timeframe
        )

        now = context.get_metadata("now")

        if now is None:
            now = datetime.now(timezone.utc)

        if now.tzinfo is None:
            now = now.replace(
                tzinfo=timezone.utc
            )

        def candle_is_closed(candle):
            """
            A confirmation candle is eligible only after
            its complete timeframe interval has elapsed.
            """

            if timeframe_seconds is None:
                return False

            try:
                candle_time = datetime.fromisoformat(
                    str(candle.time).replace(
                        "Z",
                        "+00:00",
                    )
                )
            except (
                TypeError,
                ValueError,
            ):
                return False

            if candle_time.tzinfo is None:
                candle_time = candle_time.replace(
                    tzinfo=timezone.utc
                )

            completion_time = (
                candle_time.timestamp()
                + timeframe_seconds
            )

            return completion_time <= now.timestamp()

        result.bullish_confirmation_candle = (
            next(
                (
                    candle
                    for candle in reversed(
                        result.bullish_engulfing
                    )
                    if (
                        result.protected_low is not None
                        and context.candles.index(candle)
                        > result.protected_low.index
                        and candle_is_closed(candle)
                    )
                ),
                None,
            )
        )

        result.bearish_confirmation_candle = (
            next(
                (
                    candle
                    for candle in reversed(
                        result.bearish_engulfing
                    )
                    if (
                        result.protected_high is not None
                        and context.candles.index(candle)
                        > result.protected_high.index
                        and candle_is_closed(candle)
                    )
                ),
                None,
            )
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
