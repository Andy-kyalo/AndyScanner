import unittest

from backend.pipeline.pipeline_result import PipelineResult


class TestPipelineResultRedaction(unittest.TestCase):
    def test_failure_message_redacts_query_credentials(self):
        result = PipelineResult()
        secret = "SYNTHETIC_PIPELINE_SECRET_123"

        result.set_failure(
            RuntimeError(f"request failed?apikey={secret}"),
            f"Pipeline failed?apikey={secret}",
        )

        summary = result.summary()
        self.assertNotIn(secret, result.message)
        self.assertNotIn(secret, summary["message"])
        self.assertNotIn(secret, summary["error"])

    def test_original_exception_is_preserved_internally(self):
        error = RuntimeError("failure?token=SYNTHETIC_TOKEN_456")
        result = PipelineResult()
        result.set_failure(error, str(error))

        self.assertIs(result.error, error)
        self.assertNotIn(
            "SYNTHETIC_TOKEN_456",
            result.summary()["error"],
        )

    def test_non_secret_failure_diagnostic_is_preserved(self):
        result = PipelineResult()
        result.set_failure(
            RuntimeError("Provider timeout after 10 seconds"),
            "Pipeline failed during Provider Stage",
        )

        summary = result.summary()
        self.assertIn("Provider Stage", summary["message"])
        self.assertEqual(
            summary["error"],
            "Provider timeout after 10 seconds",
        )


if __name__ == "__main__":
    unittest.main()
