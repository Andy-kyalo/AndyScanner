"""
confidence_engine.py

Confidence scoring engine for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""


class ConfidenceEngine:
    """
    Calculates confidence from a completed AnalysisResult.
    """

    def __init__(self, analysis):

        self.analysis = analysis

    # ==========================================
    # Calculate Confidence
    # ==========================================

    def calculate(self):

        confidence = 0

        trend = self.analysis.trend

        # ==========================================
        # Bullish Market
        # ==========================================

        if trend == "UPTREND":

            if self.analysis.bullish_bos:
                confidence += 25

            if self.analysis.bullish_choch:
                confidence += 20

            if self.analysis.bullish_order_block is not None:
                confidence += 15

            if self.analysis.bullish_fvg_count > 0:
                confidence += 15

            if self.analysis.buy_side_count > 0:
                confidence += 10

            if len(self.analysis.bullish_engulfing) > 0:
                confidence += 10

            confidence += 5

        # ==========================================
        # Bearish Market
        # ==========================================

        elif trend == "DOWNTREND":

            if self.analysis.bearish_bos:
                confidence += 25

            if self.analysis.bearish_choch:
                confidence += 20

            if self.analysis.bearish_order_block is not None:
                confidence += 15

            if self.analysis.bearish_fvg_count > 0:
                confidence += 15

            if self.analysis.sell_side_count > 0:
                confidence += 10

            if len(self.analysis.bearish_engulfing) > 0:
                confidence += 10

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