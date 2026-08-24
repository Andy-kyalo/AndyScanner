"""
pipeline_factory.py

Pipeline Factory.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.scanner_pipeline import ScannerPipeline

from backend.pipeline.stages.provider_stage import ProviderStage
from backend.pipeline.stages.mapping_stage import MappingStage
from backend.pipeline.stages.validation_stage import ValidationStage
from backend.pipeline.stages.analysis_stage import AnalysisStage
from backend.pipeline.stages.signal_stage import SignalStage
from backend.pipeline.stages.database_stage import DatabaseStage
from backend.pipeline.stages.report_stage import ReportStage
from backend.pipeline.stages.trade_setup_stage import TradeSetupStage

class PipelineFactory:
    """
    Factory responsible for constructing
    the complete Andy Scanner execution pipeline.
    """

    @staticmethod
    def create():

        pipeline = ScannerPipeline()

        # ---------------------------------------------
        # Execution Order
        # ---------------------------------------------

        pipeline.add_stage(
            ProviderStage()
        )

        pipeline.add_stage(
            MappingStage()
        )

        pipeline.add_stage(
            ValidationStage()
        )

        pipeline.add_stage(
            AnalysisStage()
        )

        pipeline.add_stage(
            SignalStage()
        )

        pipeline.add_stage(
            TradeSetupStage()
        )

        pipeline.add_stage(
            DatabaseStage()
        )

        pipeline.add_stage(
            ReportStage()
        )

        return pipeline

    @staticmethod
    def summary():

        pipeline = PipelineFactory.create()

        return pipeline.summary()
