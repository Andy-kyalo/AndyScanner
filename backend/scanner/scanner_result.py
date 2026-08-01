"""
scanner_result.py

Final scanner result returned after a completed scan.

Author: Andrew Kyalo
Project: Andy Scanner
"""


class ScannerResult:
    """
    Represents the final output of a scanner execution.
    """

    def __init__(
        self,
        market,
        timeframe,
        candles,
        analyzer,
        signal,
    ):

        self.market = market
        self.timeframe = timeframe

        self.candles = candles
        self.analyzer = analyzer
        self.signal = signal

    # ==================================================
    # Summary
    # ==================================================

    def summary(self):

        return {

            "market": self.market,

            "timeframe": self.timeframe,

            "candles": len(self.candles),

            "trend": self.analyzer.trend,

            "signal": self.signal.direction,

            "confidence": self.signal.confidence,

        }

    # ==================================================
    # Representation
    # ==================================================

    def __repr__(self):

        return (

            f"ScannerResult("

            f"{self.market}, "

            f"{self.timeframe}, "

            f"{self.signal.direction}, "

            f"{self.signal.confidence}%)"

        )