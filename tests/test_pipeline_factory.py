"""
test_pipeline_factory.py

Tests for the Andy Scanner pipeline factory.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import unittest

from backend.pipeline.pipeline_factory import PipelineFactory


class TestPipelineFactory(unittest.TestCase):

    def test_pipeline_contains_all_eight_stages(self):

        pipeline = PipelineFactory.create()

        expected_stages = [
            "Provider Stage",
            "Mapping Stage",
            "Validation Stage",
            "Analysis Stage",
            "Signal Stage",
            "Trade Setup Stage",
            "Database Stage",
            "Report Stage",
        ]

        actual_stages = [
            stage.name
            for stage in pipeline.stages
        ]

        self.assertEqual(
            actual_stages,
            expected_stages,
        )

    def test_pipeline_has_eight_stages(self):

        pipeline = PipelineFactory.create()

        self.assertEqual(
            len(pipeline),
            8,
        )

    def test_pipeline_summary_matches_stage_order(self):

        summary = PipelineFactory.summary()

        expected_stages = [
            "Provider Stage",
            "Mapping Stage",
            "Validation Stage",
            "Analysis Stage",
            "Signal Stage",
            "Trade Setup Stage",
            "Database Stage",
            "Report Stage",
        ]

        self.assertEqual(
            summary["total_stages"],
            8,
        )

        self.assertEqual(
            summary["stages"],
            expected_stages,
        )


if __name__ == "__main__":
    unittest.main()