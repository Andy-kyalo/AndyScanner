import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from backend.decision import Decision
from backend.report_manager import ReportManager
from backend.scanner.scanner_result import ScannerResult
from backend.trade_setup import TradeSetup


class MockAnalyzer:
    def trend(self):
        return "UPTREND"


class MockSignal:
    direction = "BUY"
    confidence = 80


class TestReportManager(unittest.TestCase):

    def test_scan_report_displays_final_wait_decision(self):
        setup = TradeSetup(
            market="EUR/USD",
            timeframe="M5",
            direction="BUY",
            entry=1.1050,
            stop_loss=1.1030,
            take_profit=1.1090,
            risk_reward=2.0,
            valid=False,
        )
        decision = Decision(
            market="EUR/USD",
            timeframe="M5",
            direction="WAIT",
            confidence=80,
            signal_direction="BUY",
            setup_valid=False,
            risk_valid=False,
            reason="STRUCTURALLY_INVALID",
        )
        result = ScannerResult(
            market="EUR/USD",
            timeframe="M5",
            candles=[],
            analyzer=MockAnalyzer(),
            signal=MockSignal(),
            trade_setup=setup,
            decision=decision,
        )

        output = StringIO()
        with patch(
            "backend.report_manager.print_analysis"
        ), patch(
            "backend.report_manager.print_strongest_candle"
        ), patch(
            "backend.report_manager.print_swing_highs"
        ), patch(
            "backend.report_manager.print_swing_lows"
        ), patch(
            "backend.report_manager.print_bos"
        ), patch(
            "backend.report_manager.print_market_structure"
        ), patch(
            "backend.report_manager.print_engulfing"
        ), patch(
            "backend.report_manager.print_order_blocks"
        ), patch(
            "backend.report_manager.print_choch"
        ), patch(
            "backend.report_manager.print_fvg"
        ), patch(
            "backend.report_manager.print_liquidity"
        ), patch(
            "backend.report_manager.print_signal"
        ), patch(
            "backend.report_manager.print_candles"
        ):
            with redirect_stdout(output):
                ReportManager().print_scan_report(
                    result.candles,
                    result.analyzer,
                    scan_result=result,
                )

        report = output.getvalue()
        self.assertIn("Original Signal", report)
        self.assertIn("BUY", report)
        self.assertIn("Final Decision", report)
        self.assertIn("WAIT", report)
        self.assertIn("Setup Valid", report)
        self.assertIn("Risk Valid", report)
        self.assertIn("STRUCTURALLY_INVALID", report)
        self.assertIn("1.105", report)
        self.assertIn("1.103", report)
        self.assertIn("1.109", report)


if __name__ == "__main__":
    unittest.main()
