"""
report_stage.py

Report Pipeline Stage.
Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_stage import PipelineStage
from backend.report_manager import ReportManager


class ReportStage(PipelineStage):
    """
    Prepares the reporting service for the completed scan.
    """

    def __init__(self):
        super().__init__("Report Stage")
        self.report_manager = ReportManager()

    def execute(self, context):
        """
        Attach the reporting service without claiming output was rendered.
        """

        context.report_manager = self.report_manager
        context.report = self.report_manager

        context.set_metadata(
            "report",
            "PREPARED",
        )

        return context
