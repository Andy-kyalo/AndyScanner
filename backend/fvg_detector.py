"""
fvg_detector.py

Fair Value Gap (FVG) detector.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from typing import List, Dict

from backend.candle import Candle


class FVGDetector:
    """
    Detects Bullish and Bearish Fair Value Gaps.
    """

    def __init__(self, candles: List[Candle]):

        if len(candles) < 3:
            raise ValueError(
                "At least 3 candles are required."
            )

        self.candles = candles

    # ==================================================
    # Bullish FVG
    # ==================================================

    def bullish_fvg(self) -> List[Dict]:

        gaps = []

        for i in range(len(self.candles) - 2):

            first = self.candles[i]
            second = self.candles[i + 1]
            third = self.candles[i + 2]

            if third.low > first.high:

                gaps.append({
                    "type": "BULLISH",
                    "first": first,
                    "middle": second,
                    "third": third,
                    "gap_top": third.low,
                    "gap_bottom": first.high,
                    "gap_size": round(
                        third.low - first.high,
                        2,
                    ),
                })

        return gaps

    # ==================================================
    # Bearish FVG
    # ==================================================

    def bearish_fvg(self) -> List[Dict]:

        gaps = []

        for i in range(len(self.candles) - 2):

            first = self.candles[i]
            second = self.candles[i + 1]
            third = self.candles[i + 2]

            if third.high < first.low:

                gaps.append({
                    "type": "BEARISH",
                    "first": first,
                    "middle": second,
                    "third": third,
                    "gap_top": first.low,
                    "gap_bottom": third.high,
                    "gap_size": round(
                        first.low - third.high,
                        2,
                    ),
                })

        return gaps

    # ==================================================
    # Latest Bullish FVG
    # ==================================================

    def latest_bullish_fvg(self):

        gaps = self.bullish_fvg()

        if gaps:
            return gaps[-1]

        return None

    # ==================================================
    # Latest Bearish FVG
    # ==================================================

    def latest_bearish_fvg(self):

        gaps = self.bearish_fvg()

        if gaps:
            return gaps[-1]

        return None

    # ==================================================
    # Statistics
    # ==================================================

    def bullish_count(self):

        return len(self.bullish_fvg())

    def bearish_count(self):

        return len(self.bearish_fvg())