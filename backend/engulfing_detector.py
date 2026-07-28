"""
engulfing_detector.py

Detects Bullish and Bearish Engulfing patterns.

Author: Andrew Kyalo
Project: Andy Scanner
"""


class EngulfingDetector:

    def __init__(self, candles):
        self.candles = candles

    def bullish_engulfing(self):

        patterns = []

        for i in range(1, len(self.candles)):

            previous = self.candles[i - 1]
            current = self.candles[i]

            if (
                previous.is_bearish()
                and current.is_bullish()
                and current.open < previous.close
                and current.close > previous.open
            ):
                patterns.append(current)

        return patterns

    def bearish_engulfing(self):

        patterns = []

        for i in range(1, len(self.candles)):

            previous = self.candles[i - 1]
            current = self.candles[i]

            if (
                previous.is_bullish()
                and current.is_bearish()
                and current.open > previous.close
                and current.close < previous.open
            ):
                patterns.append(current)

        return patterns