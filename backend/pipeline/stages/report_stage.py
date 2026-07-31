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
    Generates and displays the final scan report.
    """

    def __init__(self):

        super().__init__("Report Stage")

        self.report_manager = ReportManager()

    def execute(self, context):
        """
        Display the scanner report.
        """

        self.report_manager.print_scan_report(
            context.candles,
            context.analyzer,
        )

        self.report_manager.print_database_report()

        context.report = self.report_manager

        context.set_metadata(
            "report",
            "GENERATED",
        )

        return context