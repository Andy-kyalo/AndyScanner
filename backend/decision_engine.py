"""
decision_engine.py

Final trading decision gate for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.decision import Decision


class DecisionEngine:
    """
    Converts a generated Signal and TradeSetup validation
    into the final scanner decision.

    The engine does not perform market analysis.

    It applies the final execution gate:

        Signal
            +
        Structural Trade Setup
            +
        Risk Validation
            =
        Final Decision
    """

    BUY_DIRECTIONS = (
        "BUY",
        "STRONG BUY",
    )

    SELL_DIRECTIONS = (
        "SELL",
        "STRONG SELL",
    )

    # ==================================================
    # Generate
    # ==================================================

    def generate(
        self,
        signal,
        trade_setup,
        validation,
    ):
        """
        Generate the final trading decision.
        """

        # ==================================================
        # Missing Signal
        # ==================================================

        if signal is None:

            return Decision(
                market=None,
                timeframe=None,
                direction="WAIT",
                confidence=0,
                signal_direction=None,
                setup_valid=False,
                risk_valid=False,
                risk_reward=None,
                reason="SIGNAL_MISSING",
            )

        market = signal.market
        timeframe = signal.timeframe
        signal_direction = signal.direction
        confidence = signal.confidence

        # ==================================================
        # WAIT Signal
        # ==================================================

        if signal_direction == "WAIT":

            return Decision(
                market=market,
                timeframe=timeframe,
                direction="WAIT",
                confidence=confidence,
                signal_direction=signal_direction,
                setup_valid=(
                    trade_setup.valid
                    if trade_setup is not None
                    else False
                ),
                risk_valid=False,
                risk_reward=(
                    validation.risk_reward
                    if validation is not None
                    else None
                ),
                reason=(
                    validation.reason
                    if validation is not None
                    else "WAIT_SIGNAL"
                ),
            )

        # ==================================================
        # Missing Trade Setup
        # ==================================================

        if trade_setup is None:

            return self._rejected(
                signal,
                "TRADE_SETUP_MISSING",
            )

        # ==================================================
        # Structural Validation
        # ==================================================

        if not trade_setup.valid:

            return self._rejected(
                signal,
                "STRUCTURALLY_INVALID",
                setup_valid=False,
            )

        # ==================================================
        # Missing Risk Validation
        # ==================================================

        if validation is None:

            return self._rejected(
                signal,
                "RISK_VALIDATION_MISSING",
            )

        # ==================================================
        # Risk Validation Failed
        # ==================================================

        if not validation.valid:

            return self._rejected(
                signal,
                validation.reason,
                risk_reward=validation.risk_reward,
                setup_valid=trade_setup.valid,
            )

        # ==================================================
        # Accepted BUY / SELL
        # ==================================================

        if signal_direction in (
            self.BUY_DIRECTIONS
            + self.SELL_DIRECTIONS
        ):

            return Decision(
                market=market,
                timeframe=timeframe,
                direction=signal_direction,
                confidence=confidence,
                signal_direction=signal_direction,
                setup_valid=True,
                risk_valid=True,
                risk_reward=validation.risk_reward,
                reason="ACCEPTED",
            )

        # ==================================================
        # Unsupported Signal
        # ==================================================

        return self._rejected(
            signal,
            "UNSUPPORTED_DIRECTION",
            risk_reward=validation.risk_reward,
            setup_valid=trade_setup.valid,
        )

    # ==================================================
    # Rejected
    # ==================================================

    def _rejected(
        self,
        signal,
        reason,
        risk_reward=None,
        setup_valid=False,
    ):
        """
        Build a rejected WAIT decision.
        """

        return Decision(
            market=signal.market,
            timeframe=signal.timeframe,
            direction="WAIT",
            confidence=signal.confidence,
            signal_direction=signal.direction,
            setup_valid=setup_valid,
            risk_valid=False,
            risk_reward=risk_reward,
            reason=reason,
        )
