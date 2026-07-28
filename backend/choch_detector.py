"""
choch_detector.py

Change of Character (CHoCH) detector.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from typing import List

from backend.candle import Candle
from backend.bos_detector import BOSDetector


class CHOCHDetector:
    """
    Detects Change of Character (CHoCH).
    """

    def __init__(self, candles: List[Candle]):

        if len(candles) < 3:
            raise ValueError(
                "At least 3 candles are required."
            )

        self.candles = candles
        self.bos = BOSDetector(candles)

    # ==================================================
    # Market Trend
    # ==================================================

    def trend(self) -> str:

        first_close = self.candles[0].close
        last_close = self.candles[-1].close

        if last_close > first_close:
            return "UPTREND"

        if last_close < first_close:
            return "DOWNTREND"

        return "SIDEWAYS"

    # ==================================================
    # Bullish CHoCH
    # ==================================================

    def bullish_choch(self) -> bool:

        return (
            self.trend() == "DOWNTREND"
            and self.bos.bullish_bos()
        )

    # ==================================================
    # Bearish CHoCH
    # ==================================================

    def bearish_choch(self) -> bool:

        return (
            self.trend() == "UPTREND"
            and self.bos.bearish_bos()
        )

    # ==================================================
    # Structure
    # ==================================================

    def structure(self) -> str:

        if self.bullish_choch():
            return "BULLISH_CHOCH"

        if self.bearish_choch():
            return "BEARISH_CHOCH"

        return "NO_CHOCH"