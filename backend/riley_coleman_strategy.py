"""
riley_coleman_strategy.py

Riley Coleman reversal-strategy gate.

This module does not replace the existing market-analysis
detectors or confidence engine. It determines whether the
available analysis contains the minimum structural evidence
required for a Riley-style reversal signal.

Author: Andrew Kyalo
Project: Andy Scanner
"""


class RileyColemanStrategy:
    """
    Evaluates the currently available Riley Coleman
    reversal conditions.

    The strategy is deliberately a gate:

        valid reversal evidence -> direction
        otherwise               -> WAIT

    Generic confidence must never create a Riley BUY/SELL
    by itself.
    """

    BUY = "BUY"
    SELL = "SELL"
    WAIT = "WAIT"

    def __init__(self, analysis):
        self.analysis = analysis

    # ==================================================
    # PUBLIC
    # ==================================================

    def evaluate(self):
        """
        Return BUY, SELL, or WAIT.

        Bullish reversal:
            - existing bearish trend
            - bullish structural change
            - bullish confirmation candle

        Bearish reversal:
            - existing bullish trend
            - bearish structural change
            - bearish confirmation candle
        """

        if self._bullish_reversal():
            return self.BUY

        if self._bearish_reversal():
            return self.SELL

        return self.WAIT

    # ==================================================
    # BULLISH REVERSAL
    # ==================================================

    def _bullish_reversal(self):

        if self.analysis.trend != "DOWNTREND":
            return False

        if not self.analysis.bullish_choch:
            return False

        return (
            self.analysis.bullish_confirmation_candle
            is not None
        )

    # ==================================================
    # BEARISH REVERSAL
    # ==================================================

    def _bearish_reversal(self):

        if self.analysis.trend != "UPTREND":
            return False

        if not self.analysis.bearish_choch:
            return False

        return (
            self.analysis.bearish_confirmation_candle
            is not None
        )
