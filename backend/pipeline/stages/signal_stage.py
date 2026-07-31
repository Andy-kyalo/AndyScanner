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
    Generates the trading signal from
    the completed market analysis.
    """

    def __init__(self):

        super().__init__("Signal Stage")

    def execute(self, context):
        """
        Generate trading signal.
        """

        signal_engine = SignalEngine(
            context.analyzer
        )

        signal = signal_engine.generate()

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