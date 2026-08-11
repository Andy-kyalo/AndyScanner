"""
validation_stage.py

Validation Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""

from backend.pipeline.pipeline_stage import PipelineStage
from backend.validation.market_validator import MarketValidator


class ValidationStage(PipelineStage):
    """
    Validates market data before analysis.
    """

    def __init__(self):
        super().__init__("Validation Stage")

    def execute(self, context):

        validator = MarketValidator()

        valid, message = validator.validate(
            context.candles,
            context.timeframe,
        )

        if not valid:
            raise ValueError(
                message
            )

        context.validator = validator

        context.set_metadata(
            "validation",
            "PASSED",
        )

        context.set_metadata(
            "validation_message",
            "Market data validation passed.",
        )

        return context
