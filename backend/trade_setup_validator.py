"""
trade_setup_validator.py

Risk and quality validation for Andy Scanner trade setups.

Author: Andrew Kyalo
Project: Andy Scanner
"""


class TradeSetupValidationResult:
    """
    Represents the result of TradeSetup risk/quality validation.

    This is intentionally separate from TradeSetup.valid.

    TradeSetup.valid answers:
        "Are the entry, stop-loss and take-profit structurally valid?"

    This result answers:
        "Does the setup satisfy the configured trading-quality rules?"
    """

    def __init__(
        self,
        valid=False,
        reason=None,
        risk_reward=None,
    ):

        self.valid = valid
        self.reason = reason
        self.risk_reward = risk_reward

    # ==================================================
    # Summary
    # ==================================================

    def summary(self):

        return {
            "valid": self.valid,
            "reason": self.reason,
            "risk_reward": self.risk_reward,
        }

    # ==================================================
    # Representation
    # ==================================================

    def __repr__(self):

        return (
            "TradeSetupValidationResult("
            f"valid={self.valid}, "
            f"reason={self.reason}, "
            f"risk_reward={self.risk_reward})"
        )


class TradeSetupValidator:
    """
    Validates the risk and quality of a TradeSetup.

    The validator does not modify the supplied TradeSetup.

    Parameters
    ----------
    min_risk_reward : float
        Minimum acceptable risk/reward ratio.
    """

    BUY_DIRECTIONS = (
        "BUY",
        "STRONG BUY",
    )

    SELL_DIRECTIONS = (
        "SELL",
        "STRONG SELL",
    )

    def __init__(self, min_risk_reward=1.0):

        if min_risk_reward <= 0:
            raise ValueError(
                "Minimum risk/reward must be greater than zero."
            )

        self.min_risk_reward = float(
            min_risk_reward
        )

    # ==================================================
    # Validate
    # ==================================================

    def validate(self, setup):
        """
        Validate a complete TradeSetup.

        Returns
        -------
        TradeSetupValidationResult
        """

        if setup is None:

            return self._invalid(
                "TRADE_SETUP_MISSING"
            )

        if not setup.valid:

            return self._invalid(
                "STRUCTURALLY_INVALID"
            )

        if setup.entry is None:

            return self._invalid(
                "ENTRY_MISSING"
            )

        if setup.stop_loss is None:

            return self._invalid(
                "STOP_LOSS_MISSING"
            )

        if setup.take_profit is None:

            return self._invalid(
                "TAKE_PROFIT_MISSING"
            )

        direction = setup.direction

        if direction in self.BUY_DIRECTIONS:

            if not (
                setup.stop_loss
                < setup.entry
                < setup.take_profit
            ):

                return self._invalid(
                    "INVALID_BUY_LEVEL_RELATIONSHIP"
                )

        elif direction in self.SELL_DIRECTIONS:

            if not (
                setup.take_profit
                < setup.entry
                < setup.stop_loss
            ):

                return self._invalid(
                    "INVALID_SELL_LEVEL_RELATIONSHIP"
                )

        else:

            return self._invalid(
                "UNSUPPORTED_DIRECTION"
            )

        risk = abs(
            setup.entry
            - setup.stop_loss
        )

        reward = abs(
            setup.take_profit
            - setup.entry
        )

        if risk <= 0:

            return self._invalid(
                "ZERO_RISK"
            )

        if reward <= 0:

            return self._invalid(
                "ZERO_REWARD"
            )

        risk_reward = round(
            reward / risk,
            2,
        )

        if risk_reward < self.min_risk_reward:

            return TradeSetupValidationResult(
                valid=False,
                reason="RISK_REWARD_BELOW_MINIMUM",
                risk_reward=risk_reward,
            )

        return TradeSetupValidationResult(
            valid=True,
            reason="ACCEPTED",
            risk_reward=risk_reward,
        )

    # ==================================================
    # Convenience
    # ==================================================

    def is_valid(self, setup):

        return self.validate(
            setup
        ).valid

    # ==================================================
    # Internal
    # ==================================================

    def _invalid(self, reason):

        return TradeSetupValidationResult(
            valid=False,
            reason=reason,
            risk_reward=None,
        )