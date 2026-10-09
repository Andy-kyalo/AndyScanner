"""
pipeline_result.py

Pipeline execution result.
"""

from datetime import datetime

from backend.log_redaction import redact_secrets


class PipelineResult:
    """Represents the outcome of a pipeline execution."""

    def __init__(self):
        self.success = True
        self.message = ""
        self.error = None
        self.started_at = datetime.now()
        self.finished_at = None
        self.metadata = {}

    def set_success(self, message="Completed successfully."):
        self.success = True
        self.message = redact_secrets(message)
        self.finished_at = datetime.now()

    def set_failure(self, error, message="Execution failed."):
        self.success = False
        # Preserve the original exception for internal debugging.
        self.error = error
        self.message = redact_secrets(message)
        self.finished_at = datetime.now()

    def add_metadata(self, key, value):
        self.metadata[key] = value

    @property
    def duration(self):
        if self.finished_at is None:
            return 0.0

        return round(
            (self.finished_at - self.started_at).total_seconds(),
            3,
        )

    def summary(self):
        return {
            "success": self.success,
            "message": redact_secrets(self.message),
            "duration": self.duration,
            "error": (
                redact_secrets(str(self.error))
                if self.error
                else None
            ),
            "metadata": dict(self.metadata),
        }

    def __repr__(self):
        status = "SUCCESS" if self.success else "FAILED"
        return (
            f"PipelineResult("
            f"status={status}, "
            f"duration={self.duration}s)"
        )
