"""
pipeline_result.py

Pipeline execution result.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime


class PipelineResult:
    """
    Represents the outcome of a pipeline execution.
    """

    def __init__(self):

        self.success = True

        self.message = ""

        self.error = None

        self.started_at = datetime.now()

        self.finished_at = None

        self.metadata = {}

    # ==================================================
    # Success
    # ==================================================

    def set_success(
        self,
        message="Completed successfully.",
    ):

        self.success = True

        self.message = message

        self.finished_at = datetime.now()

    # ==================================================
    # Failure
    # ==================================================

    def set_failure(
        self,
        error,
        message="Execution failed.",
    ):

        self.success = False

        self.error = error

        self.message = message

        self.finished_at = datetime.now()

    # ==================================================
    # Metadata
    # ==================================================

    def add_metadata(
        self,
        key,
        value,
    ):

        self.metadata[key] = value

    # ==================================================
    # Duration
    # ==================================================

    @property
    def duration(self):

        if self.finished_at is None:

            return 0.0

        return round(

            (
                self.finished_at
                - self.started_at
            ).total_seconds(),

            3,

        )

    # ==================================================
    # Summary
    # ==================================================

    def summary(self):

        return {

            "success": self.success,

            "message": self.message,

            "duration": self.duration,

            "error": (
                str(self.error)
                if self.error
                else None
            ),

            "metadata": dict(self.metadata),

        }

    # ==================================================
    # Representation
    # ==================================================

    def __repr__(self):

        status = "SUCCESS" if self.success else "FAILED"

        return (
            f"PipelineResult("
            f"status={status}, "
            f"duration={self.duration}s)"
        )