import os
import tempfile
import unittest
from types import SimpleNamespace

from database.database_manager import DatabaseManager


class TestDatabaseStatistics(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = os.path.join(
            self.temp_dir.name,
            "statistics_test.db",
        )
        self.database = DatabaseManager(self.database_path)
        self.database.__enter__()

    def tearDown(self):
        self.database.__exit__(None, None, None)
        self.temp_dir.cleanup()

    def save_decision(
        self,
        direction,
        setup_valid,
        risk_valid,
        reason="ACCEPTED",
    ):
        setup = SimpleNamespace(
            entry=1.1000,
            stop_loss=1.0950,
            take_profit=1.1100,
            risk_reward=2.0,
            valid=setup_valid,
        )
        decision = SimpleNamespace(
            direction=direction,
            confidence=80,
            reason=reason,
            risk_valid=risk_valid,
        )
        self.database.save_scan(
            market="EUR/USD",
            timeframe="M5",
            trend="UPTREND",
            signal=direction,
            confidence=80,
            trade_setup=setup,
            decision=decision,
        )

    def test_empty_database_returns_zero_statistics(self):
        stats = self.database.get_database_statistics()

        self.assertEqual(stats["total_scans"], 0)
        self.assertEqual(stats["total_signals"], 0)
        self.assertEqual(stats["average_confidence"], 0)
        self.assertEqual(stats["accepted_decisions"], 0)
        self.assertEqual(stats["non_trade_decisions"], 0)

    def test_accepted_decision_requires_valid_setup_and_risk(self):
        self.save_decision("BUY", True, True)
        self.save_decision("SELL", False, True, "INVALID_SETUP")
        self.save_decision("BUY", True, False, "RISK_REJECTED")
        self.save_decision("STRONG SELL", True, True)

        stats = self.database.get_database_statistics()

        self.assertEqual(stats["accepted_decisions"], 2)

    def test_all_wait_decisions_count_as_non_trade(self):
        self.save_decision("WAIT", False, False, "STRUCTURALLY_INVALID")
        self.save_decision("WAIT", False, False, None)

        stats = self.database.get_database_statistics()

        self.assertEqual(stats["wait_decisions"], 2)
        self.assertEqual(stats["non_trade_decisions"], 2)


if __name__ == "__main__":
    unittest.main()
