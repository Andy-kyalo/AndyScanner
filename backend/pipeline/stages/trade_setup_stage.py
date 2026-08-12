"""
trade_setup_stage.py

Trade Setup Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_stage import PipelineStage
from backend.trade_setup import TradeSetup


class TradeSetupStage(PipelineStage):
    """
    Creates the initial trade setup from a generated signal.

    Detailed entry, stop-loss and take-profit calculations
    will be implemented in a later iteration.
    """

    def __init__(self):

        super().__init__("Trade Setup Stage")

    def execute(self, context):

        signal = context.signal

        setup = TradeSetup(
            market=context.market,
            timeframe=context.timeframe,
            direction=signal.direction,
        )

        context.trade_setup = setup

        context.set_metadata(
            "trade_setup",
            "CREATED",
        )

        return context
