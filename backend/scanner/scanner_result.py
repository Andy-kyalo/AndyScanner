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
        decision=None,
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
        self.decision = decision

        # Provider information
        self.provider = provider
        self.provider_symbol = provider_symbol

    # ==================================================
    # Summary
    # ==================================================

    def summary(self):
        """
        Return a compact scanner-result summary.

        The summary exposes:

            - original signal
            - trade setup
            - final decision

        The original signal is preserved separately from
        the final decision for auditability.
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
        # Final Decision
        # ==============================================

        if self.decision is not None:

            decision_direction = (
                self.decision.direction
            )

            decision_confidence = (
                self.decision.confidence
            )

            decision_reason = (
                self.decision.reason
            )

            risk_valid = (
                self.decision.risk_valid
            )

        else:

            decision_direction = None
            decision_confidence = None
            decision_reason = None
            risk_valid = False

        # ==============================================
        # Summary
        # ==============================================

        return {
            "market": self.market,
            "timeframe": self.timeframe,
            "candles": len(self.candles),
            "provider": self.provider,
            "provider_symbol": self.provider_symbol,

            # Analysis
            "trend": self.analyzer.trend(),

            # Original signal
            "signal": self.signal.direction,
            "confidence": self.signal.confidence,

            # Trade Setup
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk_reward": risk_reward,
            "setup_valid": setup_valid,

            # Final Decision
            "decision": decision_direction,
            "decision_confidence": decision_confidence,
            "decision_reason": decision_reason,
            "risk_valid": risk_valid,
        }

    # ==================================================
    # Representation
    # ==================================================

    def __repr__(self):
        """
        Return a readable representation.
        """

        decision = (
            self.decision.direction
            if self.decision is not None
            else None
        )

        return (
            f"ScannerResult("
            f"{self.market}, "
            f"{self.timeframe}, "
            f"{self.signal.direction}, "
            f"{self.signal.confidence}%, "
            f"decision={decision}, "
            f"provider={self.provider})"
        )