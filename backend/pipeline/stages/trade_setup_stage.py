"""
trade_setup_stage.py

Trade Setup Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_stage import PipelineStage
from backend.trade_setup_engine import TradeSetupEngine


class TradeSetupStage(PipelineStage):
    """
    Generates a deterministic trade setup from
    the completed analysis and trading signal.
    """

    def __init__(self):

        super().__init__("Trade Setup Stage")

    def execute(self, context):

        engine = TradeSetupEngine(
            analysis=context.analysis,
            signal=context.signal,
            candles=context.candles,
        )

        setup = engine.generate()

        context.trade_setup = setup

        context.set_metadata(
            "trade_setup",
            "VALID" if setup.valid else "INVALID",
        )

        return context
