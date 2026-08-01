"""
validation_stage.py

Validation Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_stage import PipelineStage
from backend.market_validator import MarketValidator


class ValidationStage(PipelineStage):
    """
    Validates market data before analysis.
    """

    def __init__(self):
        super().__init__("Validation Stage")

    def execute(self, context):

        validator = MarketValidator(
            context.candles
        )

        if not validator.validate():
            raise ValueError(
                "Market data validation failed."
            )

        context.validator = validator

        context.set_metadata(
            "validation",
            "PASSED",
        )

        return context