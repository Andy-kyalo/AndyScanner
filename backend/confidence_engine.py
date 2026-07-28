"""
confidence_engine.py

Confidence scoring engine for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""


class ConfidenceEngine:
    """
    Calculates confidence score for the current market bias.
    """

    def __init__(self, analyzer):

        self.analyzer = analyzer

    # ==========================================
    # Calculate Confidence
    # ==========================================

    def calculate(self):

        confidence = 0

        trend = self.analyzer.trend()

        # ==========================================
        # Bullish Market
        # ==========================================

        if trend == "UPTREND":

            # Break of Structure
            if self.analyzer.bullish_bos():
                confidence += 25

            # Change of Character
            if self.analyzer.bullish_choch():
                confidence += 20

            # Order Block
            if self.analyzer.has_bullish_order_block():
                confidence += 15

            # Fair Value Gap
            if self.analyzer.bullish_fvg():
                confidence += 15

            # Liquidity
            if self.analyzer.buy_side_count() > 0:
                confidence += 10

            # Engulfing Pattern
            if self.analyzer.bullish_engulfing():
                confidence += 10

            # Trend Alignment Bonus
            confidence += 5

        # ==========================================
        # Bearish Market
        # ==========================================

        elif trend == "DOWNTREND":

            # Break of Structure
            if self.analyzer.bearish_bos():
                confidence += 25

            # Change of Character
            if self.analyzer.bearish_choch():
                confidence += 20

            # Order Block
            if self.analyzer.has_bearish_order_block():
                confidence += 15

            # Fair Value Gap
            if self.analyzer.bearish_fvg():
                confidence += 15

            # Liquidity
            if self.analyzer.sell_side_count() > 0:
                confidence += 10

            # Engulfing Pattern
            if self.analyzer.bearish_engulfing():
                confidence += 10

            # Trend Alignment Bonus
            confidence += 5

        return min(confidence, 100)

    # ==========================================
    # Confidence Grade
    # ==========================================

    def grade(self):

        score = self.calculate()

        if score >= 90:
            return "A+"

        elif score >= 80:
            return "A"

        elif score >= 70:
            return "B"

        elif score >= 60:
            return "C"

        elif score >= 50:
            return "D"

        return "F"