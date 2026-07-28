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
    Generates trading signals from
    Analyzer and ConfidenceEngine.
    """

    def __init__(self, analyzer):

        self.analyzer = analyzer
        self.confidence = ConfidenceEngine(analyzer)

    # ==========================================
    # Generate Signal
    # ==========================================

    def generate(self):

        score = self.confidence.calculate()

        trend = self.analyzer.trend()

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
            market="US30",
            timeframe="M5",
            direction=direction,
            confidence=score,
        )