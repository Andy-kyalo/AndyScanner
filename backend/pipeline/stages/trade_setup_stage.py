"""
trade_setup_stage.py

Trade Setup Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_stage import PipelineStage
from backend.trade_setup_engine import TradeSetupEngine
from backend.trade_setup_validator import TradeSetupValidator


class TradeSetupStage(PipelineStage):
    """
    Generates and validates a deterministic trade setup.

    TradeSetupEngine is responsible for constructing the
    structural setup.

    TradeSetupValidator is responsible for determining
    whether the setup satisfies the configured
    risk/quality requirements.
    """

    def __init__(
        self,
        min_risk_reward=1.0,
    ):

        super().__init__("Trade Setup Stage")

        self.validator = TradeSetupValidator(
            min_risk_reward=min_risk_reward
        )

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
        # Risk / Quality Validation
        # ==================================================

        validation = self.validator.validate(
            setup
        )

        context.trade_setup_validation = validation

        # ==================================================
        # Metadata
        # ==================================================

        context.set_metadata(
            "trade_setup",
            "VALID" if setup.valid else "INVALID",
        )

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

        return context
