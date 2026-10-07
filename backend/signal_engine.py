"""
signal_engine.py

Riley Coleman strategy signal engine.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.signal import Signal
from backend.confidence_engine import ConfidenceEngine
from backend.riley_coleman_strategy import RileyColemanStrategy


class SignalEngine:
    """
    Generates signals from completed market analysis.

    Confidence is retained as a measurement, but it is no
    longer sufficient by itself to create a BUY or SELL.

    The Riley Coleman strategy is the directional gate.
    """

    def __init__(self, analysis):

        self.analysis = analysis

        self.confidence = ConfidenceEngine(
            analysis
        )

        self.strategy = RileyColemanStrategy(
            analysis
        )

    # ==========================================
    # Generate Signal
    # ==========================================

    def generate(self):

        score = self.confidence.calculate()

        direction = self.strategy.evaluate()

        return Signal(
            market=self.analysis.market,
            timeframe=self.analysis.timeframe,
            direction=direction,
            confidence=score,
        )
