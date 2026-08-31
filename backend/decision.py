"""
decision.py

Final trading decision produced after signal generation
and trade setup risk validation.

Author: Andrew Kyalo
Project: Andy Scanner
"""


class Decision:
    """
    Represents the final trading decision.

    The original signal remains separate from the final
    decision so that the scanner can distinguish between:

        - what the analysis suggested
        - whether the trade setup was acceptable
        - what the final executable decision is
    """

    VALID_DIRECTIONS = (
        "BUY",
        "STRONG BUY",
        "SELL",
        "STRONG SELL",
        "WAIT",
    )

    def __init__(
        self,
        market,
        timeframe,
        direction,
        confidence,
        signal_direction,
        setup_valid=False,
        risk_valid=False,
        risk_reward=None,
        reason=None,
    ):
        self.market = market
        self.timeframe = timeframe

        self.direction = direction
        self.confidence = confidence

        self.signal_direction = signal_direction

        self.setup_valid = setup_valid
        self.risk_valid = risk_valid

        self.risk_reward = risk_reward

        self.reason = reason

    # ==================================================
    # Summary
    # ==================================================

    def summary(self):
        """
        Return a machine-readable decision summary.
        """

        return {
            "market": self.market,
            "timeframe": self.timeframe,
            "direction": self.direction,
            "confidence": self.confidence,
            "signal_direction": self.signal_direction,
            "setup_valid": self.setup_valid,
            "risk_valid": self.risk_valid,
            "risk_reward": self.risk_reward,
            "reason": self.reason,
        }

    # ==================================================
    # Representation
    # ==================================================

    def __repr__(self):
        """
        Return a readable representation.
        """

        return (
            "Decision("
            f"market={self.market}, "
            f"timeframe={self.timeframe}, "
            f"direction={self.direction}, "
            f"confidence={self.confidence}%, "
            f"signal_direction={self.signal_direction}, "
            f"setup_valid={self.setup_valid}, "
            f"risk_valid={self.risk_valid}, "
            f"risk_reward={self.risk_reward}, "
            f"reason={self.reason})"
        )