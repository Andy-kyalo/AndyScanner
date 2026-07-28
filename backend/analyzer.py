"""
analyzer.py

Market Analysis Coordinator.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.swing_detector import SwingDetector
from backend.bos_detector import BOSDetector
from backend.choch_detector import CHOCHDetector
from backend.engulfing_detector import EngulfingDetector
from backend.fvg_detector import FVGDetector
from backend.liquidity_detector import LiquidityDetector
from backend.order_block_detector import OrderBlockDetector
from backend.signal_engine import SignalEngine


class Analyzer:
    """
    Central market analysis engine.

    Coordinates every detector and exposes a
    single interface for the scanner.
    """

    def __init__(self, candles):

        self.candles = candles

        self.swing = SwingDetector(candles)
        self.bos = BOSDetector(candles)
        self.choch = CHOCHDetector(candles)
        self.engulfing = EngulfingDetector(candles)
        self.fvg = FVGDetector(candles)
        self.liquidity = LiquidityDetector(candles)
        self.order_block = OrderBlockDetector(candles)

    # ==================================================
    # MARKET STATISTICS
    # ==================================================

    def highest_high(self):
        return max(candle.high for candle in self.candles)

    def lowest_low(self):
        return min(candle.low for candle in self.candles)

    def trend(self):
        return self.choch.trend()

    def strongest_candle(self):
        return max(
            self.candles,
            key=lambda candle: candle.body_size()
        )

    # ==================================================
    # SWINGS
    # ==================================================

    def swing_highs(self):
        return self.swing.swing_highs()

    def swing_lows(self):
        return self.swing.swing_lows()

    # ==================================================
    # BREAK OF STRUCTURE
    # ==================================================

    def bullish_bos(self):
        return self.bos.bullish_bos()

    def bearish_bos(self):
        return self.bos.bearish_bos()

    # ==================================================
    # CHANGE OF CHARACTER
    # ==================================================

    def bullish_choch(self):
        return self.choch.bullish_choch()

    def bearish_choch(self):
        return self.choch.bearish_choch()

    # ==================================================
    # ENGULFING PATTERNS
    # ==================================================

    def bullish_engulfing(self):
        return self.engulfing.bullish_engulfing()

    def bearish_engulfing(self):
        return self.engulfing.bearish_engulfing()

    # ==================================================
    # FAIR VALUE GAPS
    # ==================================================

    def bullish_fvg(self):
        return self.fvg.bullish_fvg()

    def bearish_fvg(self):
        return self.fvg.bearish_fvg()

    # ==================================================
    # LIQUIDITY
    # ==================================================

    def buy_side_liquidity(self):
        return self.liquidity.buy_side_liquidity()

    def sell_side_liquidity(self):
        return self.liquidity.sell_side_liquidity()

    def latest_buy_side_liquidity(self):
        return self.liquidity.latest_buy_side()

    def latest_sell_side_liquidity(self):
        return self.liquidity.latest_sell_side()

    def buy_side_count(self):
        return self.liquidity.buy_side_count()

    def sell_side_count(self):
        return self.liquidity.sell_side_count()

    # ==================================================
    # ORDER BLOCKS
    # ==================================================

    def bullish_order_block(self):
        return self.order_block.bullish_order_block()

    def bearish_order_block(self):
        return self.order_block.bearish_order_block()

    def has_bullish_order_block(self):
        return self.order_block.has_bullish_order_block()

    def has_bearish_order_block(self):
        return self.order_block.has_bearish_order_block()

    # ==================================================
    # SIGNAL ENGINE
    # ==================================================

    def generate_signal(self):
        """
        Generates the final trading signal using the
        dedicated Signal Engine.
        """

        engine = SignalEngine(self)
        return engine.generate()