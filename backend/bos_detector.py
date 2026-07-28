"""
bos_detector.py

Break of Structure (BOS) detector.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from typing import List

from backend.candle import Candle
from backend.swing_detector import SwingDetector


class BOSDetector:
    """
    Detects bullish and bearish Break of Structure.
    """

    def __init__(self, candles: List[Candle]):

        if len(candles) < 3:
            raise ValueError(
                "At least 3 candles are required."
            )

        self.candles = candles
        self.swing_detector = SwingDetector(candles)

    # ==================================================
    # Bullish BOS
    # ==================================================

    def bullish_bos(self) -> bool:

        latest_high = self.swing_detector.latest_swing_high()

        if latest_high is None:
            return False

        last_candle = self.candles[-1]

        return last_candle.close > latest_high.high

    # ==================================================
    # Bearish BOS
    # ==================================================

    def bearish_bos(self) -> bool:

        latest_low = self.swing_detector.latest_swing_low()

        if latest_low is None:
            return False

        last_candle = self.candles[-1]

        return last_candle.close < latest_low.low

    # ==================================================
    # Market Structure
    # ==================================================

    def structure(self) -> str:

        if self.bullish_bos():
            return "BULLISH_BOS"

        if self.bearish_bos():
            return "BEARISH_BOS"

        return "NO_BOS"