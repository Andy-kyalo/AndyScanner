"""
swing_detector.py

Detects swing highs and swing lows.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from typing import List, Optional

from backend.candle import Candle


class SwingDetector:
    """
    Detects swing highs and swing lows from market candles.
    """

    def __init__(self, candles: List[Candle]):

        if len(candles) < 3:
            raise ValueError(
                "At least 3 candles are required."
            )

        self.candles = candles

    # ==================================================
    # Swing Highs
    # ==================================================

    def swing_highs(self) -> List[Candle]:

        swings = []

        for i in range(1, len(self.candles) - 1):

            previous = self.candles[i - 1]
            current = self.candles[i]
            next_candle = self.candles[i + 1]

            if (
                current.high > previous.high
                and current.high > next_candle.high
            ):
                swings.append(current)

        return swings

    # ==================================================
    # Swing Lows
    # ==================================================

    def swing_lows(self) -> List[Candle]:

        swings = []

        for i in range(1, len(self.candles) - 1):

            previous = self.candles[i - 1]
            current = self.candles[i]
            next_candle = self.candles[i + 1]

            if (
                current.low < previous.low
                and current.low < next_candle.low
            ):
                swings.append(current)

        return swings

    # ==================================================
    # Latest Swing High
    # ==================================================

    def latest_swing_high(self) -> Optional[Candle]:

        highs = self.swing_highs()

        if highs:
            return highs[-1]

        return None

    # ==================================================
    # Latest Swing Low
    # ==================================================

    def latest_swing_low(self) -> Optional[Candle]:

        lows = self.swing_lows()

        if lows:
            return lows[-1]

        return None

    # ==================================================
    # Statistics
    # ==================================================

    def total_swing_highs(self) -> int:

        return len(self.swing_highs())

    def total_swing_lows(self) -> int:

        return len(self.swing_lows())