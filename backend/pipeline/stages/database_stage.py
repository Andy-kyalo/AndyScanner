"""
database_stage.py

Database Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_stage import PipelineStage
from config.config import Config
from database.database_manager import DatabaseManager


class DatabaseStage(PipelineStage):
    """
    Saves completed scan results into the database.
    """

    def __init__(self):

        super().__init__("Database Stage")

    def execute(self, context):
        """
        Persist scan results.
        """

        with DatabaseManager(Config.DATABASE_PATH) as database:

            database.save_scan(

                market=context.market,

                timeframe=context.timeframe,

                trend=context.analyzer.trend(),

                signal=context.signal.direction,

                confidence=context.signal.confidence,

            )

        context.set_metadata(

            "database",

            "SAVED",

        )

        return context