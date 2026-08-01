"""
database_stage.py

Database Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime

from backend.pipeline.pipeline_stage import PipelineStage
from database.database_manager import DatabaseManager


class DatabaseStage(PipelineStage):
    """
    Saves scan results into the database.
    """

    def __init__(self):

        super().__init__("Database Stage")

    def execute(self, context):

        scan_time = datetime.now()

        with DatabaseManager() as database:

            exists = database.scan_exists(
                context.market,
                context.timeframe,
                scan_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            )

            if not exists:

                database.save_signal(
                    context.signal
                )

                database.save_scan(
                    market=context.market,
                    timeframe=context.timeframe,
                    trend=context.trend,
                    signal=context.signal.direction,
                    confidence=context.signal.confidence,
                )

                context.set_metadata(
                    "database",
                    "SAVED",
                )

            else:

                context.set_metadata(
                    "database",
                    "DUPLICATE",
                )

        return context