import os
import tempfile
import unittest
from types import SimpleNamespace

from database.database_manager import DatabaseManager


class TestDatabasePersistenceSafety(unittest.TestCase):

    def test_rollback_removes_signal_when_scan_write_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            database_path = os.path.join(
                directory,
                "persistence_test.db",
            )

            signal = SimpleNamespace(
                market="EUR/USD",
                timeframe="M5",
                direction="BUY",
                confidence=80,
            )

            database = DatabaseManager(database_path)

            with database:
                try:
                    with database.transaction():
                        database.save_signal(signal)
                        raise RuntimeError("Simulated scan write failure")
                except RuntimeError:
                    pass
                else:
                    self.fail("Expected simulated persistence failure.")

                signal_count = database.connection.execute(
                    "SELECT COUNT(*) FROM signals"
                ).fetchone()[0]

                self.assertEqual(signal_count, 0)


    def test_database_stage_rolls_back_signal_when_scan_write_fails(self):
        from unittest.mock import patch

        from backend.pipeline.pipeline_context import PipelineContext
        from backend.pipeline.stages.database_stage import DatabaseStage

        with tempfile.TemporaryDirectory() as directory:
            database_path = os.path.join(
                directory,
                "database_stage_test.db",
            )

            context = PipelineContext()
            context.start("EUR/USD", "M5")
            context.signal = SimpleNamespace(
                market="EUR/USD",
                timeframe="M5",
                direction="BUY",
                confidence=80,
            )
            context.analysis = None
            context.trade_setup = None
            context.decision = None

            original_database_manager = DatabaseManager

            class FailingScanDatabaseManager(original_database_manager):
                def __init__(self):
                    super().__init__(database_path)

                def save_scan(self, *args, **kwargs):
                    raise RuntimeError("Simulated scan write failure")

            with patch(
                "backend.pipeline.stages.database_stage.DatabaseManager",
                FailingScanDatabaseManager,
            ):
                with self.assertRaisesRegex(
                    RuntimeError,
                    "Simulated scan write failure",
                ):
                    DatabaseStage().execute(context)

            with original_database_manager(database_path) as database:
                signal_count = database.connection.execute(
                    "SELECT COUNT(*) FROM signals"
                ).fetchone()[0]

                scan_count = database.connection.execute(
                    "SELECT COUNT(*) FROM scans"
                ).fetchone()[0]

            self.assertEqual(signal_count, 0)
            self.assertEqual(scan_count, 0)


if __name__ == "__main__":
    unittest.main()
