"""
validation_stage.py

Validation Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_stage import PipelineStage
from backend.validator.market_data_validator import MarketDataValidator


class ValidationStage(PipelineStage):
    """
    Validates mapped market data before analysis.
    """

    def __init__(self):

        super().__init__("Validation Stage")

        self.validator = MarketDataValidator()

    def execute(self, context):
        """
        Validate mapped candle data.
        """

        self.validator.validate(
            context.candles
        )

        context.set_metadata(
            "validation",
            "PASSED",
        )

        return context