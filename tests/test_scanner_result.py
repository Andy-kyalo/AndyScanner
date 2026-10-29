import unittest

from backend.decision import Decision
from backend.scanner.scanner_result import ScannerResult
from backend.trade_setup import TradeSetup


class MockAnalyzer:
    def trend(self):
        return "UPTREND"


class MockSignal:
    direction = "BUY"
    confidence = 75


class TestScannerResult(unittest.TestCase):

    def make_result(self, signal=None, trade_setup=None, decision=None):
        return ScannerResult(
            market="EUR/USD",
            timeframe="M5",
            candles=[object(), object()],
            analyzer=MockAnalyzer(),
            signal=signal or MockSignal(),
            trade_setup=trade_setup,
            decision=decision,
            provider="TwelveData",
            provider_symbol="EUR/USD",
        )

    def test_summary_preserves_signal_setup_and_accepted_decision(self):
        setup = TradeSetup(
            market="EUR/USD",
            timeframe="M5",
            direction="BUY",
            entry=1.1050,
            stop_loss=1.1030,
            take_profit=1.1090,
            risk_reward=2.0,
            valid=True,
        )
        decision = Decision(
            market="EUR/USD",
            timeframe="M5",
            direction="BUY",
            confidence=80,
            signal_direction="BUY",
            setup_valid=True,
            risk_valid=True,
            risk_reward=2.0,
            reason="ACCEPTED",
        )

        summary = self.make_result(
            trade_setup=setup,
            decision=decision,
        ).summary()

        self.assertEqual(summary["signal"], "BUY")
        self.assertEqual(summary["confidence"], 75)
        self.assertEqual(summary["candles"], 2)
        self.assertEqual(summary["provider"], "TwelveData")
        self.assertEqual(summary["provider_symbol"], "EUR/USD")
        self.assertEqual(summary["entry"], 1.1050)
        self.assertEqual(summary["stop_loss"], 1.1030)
        self.assertEqual(summary["take_profit"], 1.1090)
        self.assertEqual(summary["risk_reward"], 2.0)
        self.assertTrue(summary["setup_valid"])
        self.assertEqual(summary["decision"], "BUY")
        self.assertEqual(summary["decision_confidence"], 80)
        self.assertEqual(summary["decision_reason"], "ACCEPTED")
        self.assertTrue(summary["risk_valid"])

    def test_summary_preserves_wait_decision_without_creating_trade(self):
        setup = TradeSetup(
            market="EUR/USD",
            timeframe="M5",
            direction="WAIT",
            valid=False,
        )
        decision = Decision(
            market="EUR/USD",
            timeframe="M5",
            direction="WAIT",
            confidence=40,
            signal_direction="WAIT",
            setup_valid=False,
            risk_valid=False,
            reason="STRUCTURALLY_INVALID",
        )

        summary = self.make_result(
            trade_setup=setup,
            decision=decision,
        ).summary()

        self.assertEqual(summary["signal"], "BUY")
        self.assertEqual(summary["decision"], "WAIT")
        self.assertFalse(summary["setup_valid"])
        self.assertFalse(summary["risk_valid"])
        self.assertIsNone(summary["entry"])
        self.assertIsNone(summary["stop_loss"])
        self.assertIsNone(summary["take_profit"])
        self.assertEqual(
            summary["decision_reason"],
            "STRUCTURALLY_INVALID",
        )

    def test_summary_handles_missing_setup_and_decision(self):
        summary = self.make_result().summary()

        self.assertEqual(summary["signal"], "BUY")
        self.assertIsNone(summary["entry"])
        self.assertIsNone(summary["stop_loss"])
        self.assertIsNone(summary["take_profit"])
        self.assertIsNone(summary["risk_reward"])
        self.assertFalse(summary["setup_valid"])
        self.assertIsNone(summary["decision"])
        self.assertIsNone(summary["decision_confidence"])
        self.assertIsNone(summary["decision_reason"])
        self.assertFalse(summary["risk_valid"])


if __name__ == "__main__":
    unittest.main()
