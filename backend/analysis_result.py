"""
analysis_result.py

Structured result produced by the Analysis Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""


class AnalysisResult:
    """
    Stores the complete market-analysis snapshot.

    This object separates market analysis from
    confidence scoring and signal generation.
    """

    def __init__(self):

        # ==========================================
        # MARKET
        # ==========================================

        self.market = None
        self.timeframe = None

        # ==========================================
        # MARKET STRUCTURE
        # ==========================================

        self.trend = "SIDEWAYS"

        self.bullish_bos = False
        self.bearish_bos = False

        self.bullish_choch = False
        self.bearish_choch = False

        # ==========================================
        # PRICE ACTION
        # ==========================================

        self.bullish_engulfing = []
        self.bearish_engulfing = []

        # ==========================================
        # FAIR VALUE GAPS
        # ==========================================

        self.bullish_fvg = []
        self.bearish_fvg = []

        # ==========================================
        # LIQUIDITY
        # ==========================================

        self.buy_side_liquidity = []
        self.sell_side_liquidity = []

        # ==========================================
        # ORDER BLOCKS
        # ==========================================

        self.bullish_order_block = None
        self.bearish_order_block = None

        # ==========================================
        # PRICE STATISTICS
        # ==========================================

        self.highest_high = None
        self.lowest_low = None
        self.strongest_candle = None

    # ==========================================
    # Structure
    # ==========================================

    @property
    def structure(self):

        if self.bullish_bos:
            return "BULLISH_BOS"

        if self.bearish_bos:
            return "BEARISH_BOS"

        if self.bullish_choch:
            return "BULLISH_CHOCH"

        if self.bearish_choch:
            return "BEARISH_CHOCH"

        return "NO_STRUCTURE"

    # ==========================================
    # Liquidity Counts
    # ==========================================

    @property
    def buy_side_count(self):

        return len(self.buy_side_liquidity)

    @property
    def sell_side_count(self):

        return len(self.sell_side_liquidity)

    # ==========================================
    # FVG Counts
    # ==========================================

    @property
    def bullish_fvg_count(self):

        return len(self.bullish_fvg)

    @property
    def bearish_fvg_count(self):

        return len(self.bearish_fvg)

    # ==========================================
    # Summary
    # ==========================================

    def summary(self):

        return {
            "market": self.market,
            "timeframe": self.timeframe,
            "trend": self.trend,
            "structure": self.structure,
            "bullish_bos": self.bullish_bos,
            "bearish_bos": self.bearish_bos,
            "bullish_choch": self.bullish_choch,
            "bearish_choch": self.bearish_choch,
            "bullish_fvg_count": self.bullish_fvg_count,
            "bearish_fvg_count": self.bearish_fvg_count,
            "buy_side_count": self.buy_side_count,
            "sell_side_count": self.sell_side_count,
            "has_bullish_order_block": (
                self.bullish_order_block is not None
            ),
            "has_bearish_order_block": (
                self.bearish_order_block is not None
            ),
            "highest_high": self.highest_high,
            "lowest_low": self.lowest_low,
        }

    # ==========================================
    # Representation
    # ==========================================

    def __repr__(self):

        return (
            f"AnalysisResult("
            f"market={self.market}, "
            f"timeframe={self.timeframe}, "
            f"trend={self.trend}, "
            f"structure={self.structure})"
        )
