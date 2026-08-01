"""
analysis_stage.py

Analysis Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_stage import PipelineStage
from backend.analyzer import Analyzer


class AnalysisStage(PipelineStage):
    """
    Performs market analysis.
    """

    def __init__(self):

        super().__init__("Analysis Stage")

    def execute(self, context):

        analyzer = Analyzer(
            context.candles
        )

        context.analyzer = analyzer

        context.trend = analyzer.trend()

        context.set_metadata(
            "trend",
            context.trend,
        )

        return context