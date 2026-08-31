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
        trade_setup=None,
        provider=None,
        provider_symbol=None,
    ):
        """
        Initialize the final scanner result.
        """

        self.market = market
        self.timeframe = timeframe

        self.candles = candles
        self.analyzer = analyzer
        self.signal = signal
        self.trade_setup = trade_setup

        # Provider information
        self.provider = provider
        self.provider_symbol = provider_symbol

    # ==================================================
    # Summary
    # ==================================================

    def summary(self):
        """
        Return a compact scanner-result summary.

        Trade setup fields are exposed when a TradeSetup
        exists. If no setup exists, the values remain None
        and setup_valid is False.
        """

        # ==============================================
        # Trade Setup
        # ==============================================

        if self.trade_setup is not None:

            entry = self.trade_setup.entry
            stop_loss = self.trade_setup.stop_loss
            take_profit = self.trade_setup.take_profit
            risk_reward = self.trade_setup.risk_reward
            setup_valid = self.trade_setup.valid

        else:

            entry = None
            stop_loss = None
            take_profit = None
            risk_reward = None
            setup_valid = False

        # ==============================================
        # Summary
        # ==============================================

        return {
            "market": self.market,
            "timeframe": self.timeframe,
            "candles": len(self.candles),
            "provider": self.provider,
            "provider_symbol": self.provider_symbol,
            "trend": self.analyzer.trend(),
            "signal": self.signal.direction,
            "confidence": self.signal.confidence,

            # Trade Setup
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk_reward": risk_reward,
            "setup_valid": setup_valid,
        }

    # ==================================================
    # Representation
    # ==================================================

    def __repr__(self):
        """
        Return a readable representation.
        """

        return (
            f"ScannerResult("
            f"{self.market}, "
            f"{self.timeframe}, "
            f"{self.signal.direction}, "
            f"{self.signal.confidence}%, "
            f"provider={self.provider})"
        )