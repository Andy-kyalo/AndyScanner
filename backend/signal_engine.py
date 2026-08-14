"""
signal_engine.py

Professional trading signal engine.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.signal import Signal
from backend.confidence_engine import ConfidenceEngine


class SignalEngine:
    """
    Generates trading signals from a completed AnalysisResult.
    """

    def __init__(self, analysis):

        self.analysis = analysis

        self.confidence = ConfidenceEngine(
            analysis
        )

    # ==========================================
    # Generate Signal
    # ==========================================

    def generate(self):

        score = self.confidence.calculate()

        trend = self.analysis.trend

        direction = "WAIT"

        if trend == "UPTREND":

            if score >= 80:
                direction = "STRONG BUY"

            elif score >= 60:
                direction = "BUY"

        elif trend == "DOWNTREND":

            if score >= 80:
                direction = "STRONG SELL"

            elif score >= 60:
                direction = "SELL"

        return Signal(
            market=self.analysis.market,
            timeframe=self.analysis.timeframe,
            direction=direction,
            confidence=score,
        )