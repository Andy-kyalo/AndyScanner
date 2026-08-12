"""
signal_stage.py

Signal Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_stage import PipelineStage
from backend.signal_engine import SignalEngine


class SignalStage(PipelineStage):
    """
    Generates trading signals from analysis.
    """

    def __init__(self):

        super().__init__("Signal Stage")

    def execute(self, context):

        signal = SignalEngine(
            context.analysis
        ).generate()

        signal.market = context.market
        signal.timeframe = context.timeframe

        context.signal = signal

        context.set_metadata(
            "signal",
            signal.direction,
        )

        context.set_metadata(
            "confidence",
            signal.confidence,
        )

        return context
