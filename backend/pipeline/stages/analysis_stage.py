"""
analysis_stage.py

Analysis Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_stage import PipelineStage
from backend.analyzer.market_analyzer import MarketAnalyzer


class AnalysisStage(PipelineStage):
    """
    Performs market analysis using mapped
    and validated candle data.
    """

    def __init__(self):

        super().__init__("Analysis Stage")

    def execute(self, context):
        """
        Analyze market candles.
        """

        analyzer = MarketAnalyzer(
            context.candles
        )

        context.analyzer = analyzer

        context.set_metadata(
            "trend",
            analyzer.trend(),
        )

        context.set_metadata(
            "highest_high",
            analyzer.highest_high(),
        )

        context.set_metadata(
            "lowest_low",
            analyzer.lowest_low(),
        )

        return context