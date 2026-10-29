import unittest

from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.stages.report_stage import ReportStage
from backend.report_manager import ReportManager


class TestReportStage(unittest.TestCase):

    def test_stage_attaches_report_manager_without_claiming_rendered_output(self):
        stage = ReportStage()
        context = PipelineContext()

        result = stage.execute(context)

        self.assertIs(result, context)
        self.assertIsInstance(context.report_manager, ReportManager)
        self.assertIs(context.report, context.report_manager)

        # The stage prepares the reporting service; it does not render output.
        self.assertEqual(
            context.get_metadata("report"),
            "PREPARED",
        )


if __name__ == "__main__":
    unittest.main()
