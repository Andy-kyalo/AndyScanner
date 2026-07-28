"""
liquidity_detector.py

Liquidity detector.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from typing import List

from backend.candle import Candle
from backend.swing_detector import SwingDetector


class LiquidityDetector:
    """
    Detects buy-side and sell-side liquidity.

    Buy-side Liquidity:
        Swing Highs

    Sell-side Liquidity:
        Swing Lows
    """

    def __init__(self, candles: List[Candle]):

        if len(candles) < 3:
            raise ValueError(
                "At least 3 candles are required."
            )

        self.candles = candles
        self.swing_detector = SwingDetector(candles)

    # ==========================================
    # Buy-side Liquidity
    # ==========================================

    def buy_side_liquidity(self) -> List[Candle]:

        return self.swing_detector.swing_highs()

    # ==========================================
    # Sell-side Liquidity
    # ==========================================

    def sell_side_liquidity(self) -> List[Candle]:

        return self.swing_detector.swing_lows()

    # ==========================================
    # Latest Liquidity Levels
    # ==========================================

    def latest_buy_side(self):

        liquidity = self.buy_side_liquidity()

        return liquidity[-1] if liquidity else None

    def latest_sell_side(self):

        liquidity = self.sell_side_liquidity()

        return liquidity[-1] if liquidity else None

    # ==========================================
    # Liquidity Prices
    # ==========================================

    def buy_side_prices(self):

        return [
            candle.high
            for candle in self.buy_side_liquidity()
        ]

    def sell_side_prices(self):

        return [
            candle.low
            for candle in self.sell_side_liquidity()
        ]

    # ==========================================
    # Statistics
    # ==========================================

    def buy_side_count(self) -> int:

        return len(self.buy_side_liquidity())

    def sell_side_count(self) -> int:

        return len(self.sell_side_liquidity())

    def total_liquidity(self) -> int:

        return (
            self.buy_side_count()
            + self.sell_side_count()
        )

    # ==========================================
    # Liquidity Availability
    # ==========================================

    def has_buy_side(self) -> bool:

        return self.buy_side_count() > 0

    def has_sell_side(self) -> bool:

        return self.sell_side_count() > 0