"""
trade_setup_stage.py

Trade Setup Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_stage import PipelineStage
from backend.trade_setup_engine import TradeSetupEngine
from backend.trade_setup_validator import TradeSetupValidator
from backend.decision_engine import DecisionEngine


class TradeSetupStage(PipelineStage):
    """
    Generates the trade setup, validates its risk,
    and produces the final trading decision.

    Processing order:

        TradeSetupEngine
            ↓
        TradeSetupValidator
            ↓
        DecisionEngine
    """

    def __init__(
        self,
        min_risk_reward=1.0,
    ):

        super().__init__("Trade Setup Stage")

        self.validator = TradeSetupValidator(
            min_risk_reward=min_risk_reward
        )

        self.decision_engine = DecisionEngine()

    def execute(self, context):

        # ==================================================
        # Generate Trade Setup
        # ==================================================

        engine = TradeSetupEngine(
            analysis=context.analysis,
            signal=context.signal,
            candles=context.candles,
        )

        setup = engine.generate()

        context.trade_setup = setup

        # ==================================================
        # Structural Metadata
        # ==================================================

        context.set_metadata(
            "trade_setup",
            "VALID"
            if setup.valid
            else "INVALID",
        )

        # ==================================================
        # Risk / Quality Validation
        # ==================================================

        validation = self.validator.validate(
            setup
        )

        context.trade_setup_validation = validation

        context.set_metadata(
            "risk_validation",
            "ACCEPTED"
            if validation.valid
            else "REJECTED",
        )

        context.set_metadata(
            "risk_validation_reason",
            validation.reason,
        )

        context.set_metadata(
            "risk_validation_rr",
            validation.risk_reward,
        )

        # ==================================================
        # Final Decision Gate
        # ==================================================

        decision = self.decision_engine.generate(
            signal=context.signal,
            trade_setup=setup,
            validation=validation,
        )

        context.decision = decision

        # ==================================================
        # Decision Metadata
        # ==================================================

        context.set_metadata(
            "decision",
            decision.direction,
        )

        context.set_metadata(
            "decision_reason",
            decision.reason,
        )

        context.set_metadata(
            "decision_signal",
            decision.signal_direction,
        )

        context.set_metadata(
            "decision_confidence",
            decision.confidence,
        )

        return context