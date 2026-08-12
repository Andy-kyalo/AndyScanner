import unittest

from backend.scanner.scanner_result import ScannerResult


class MockAnalyzer:

    def trend(self):
        return "UPTREND"


class MockSignal:

    direction = "BUY"
    confidence = 75


class MockTradeSetup:

    direction = "BUY"
    market = "US30"
    timeframe = "M5"


class TestScannerResult(unittest.TestCase):

    def test_scanner_result_preserves_trade_setup(self):

        trade_setup = MockTradeSetup()

        result = ScannerResult(
            market="US30",
            timeframe="M5",
            candles=[],
            analyzer=MockAnalyzer(),
            signal=MockSignal(),
            trade_setup=trade_setup,
        )

        self.assertIs(
            result.trade_setup,
            trade_setup,
        )


if __name__ == "__main__":
    unittest.main()
