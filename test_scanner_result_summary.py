"""
test_scanner_result_summary.py

Contract tests for ScannerResult.summary().

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.candle import Candle
from backend.analysis_result import AnalysisResult
from backend.scanner.scanner_result import ScannerResult
from backend.signal import Signal
from backend.trade_setup import TradeSetup


class MockAnalyzer:

    def __init__(self, trend):
        self._trend = trend

    def trend(self):
        return self._trend


def make_candle():

    return Candle(
        time="2026-08-31 13:00:00",
        open_price=100.0,
        high=105.0,
        low=95.0,
        close=103.0,
    )


def test_valid_trade_setup_summary():

    signal = Signal(
        market="EURUSD",
        timeframe="M5",
        direction="BUY",
        confidence=80,
    )

    setup = TradeSetup(
        market="EURUSD",
        timeframe="M5",
        direction="BUY",
        entry=100.0,
        stop_loss=95.0,
        take_profit=110.0,
        risk_reward=2.0,
        valid=True,
    )

    result = ScannerResult(
        market="EURUSD",
        timeframe="M5",
        candles=[make_candle()],
        analyzer=MockAnalyzer("UPTREND"),
        signal=signal,
        trade_setup=setup,
        provider="TwelveDataProvider",
        provider_symbol="EUR/USD",
    )

    summary = result.summary()

    assert summary["market"] == "EURUSD"
    assert summary["timeframe"] == "M5"
    assert summary["candles"] == 1
    assert summary["provider"] == "TwelveDataProvider"
    assert summary["provider_symbol"] == "EUR/USD"

    assert summary["trend"] == "UPTREND"
    assert summary["signal"] == "BUY"
    assert summary["confidence"] == 80

    assert summary["entry"] == 100.0
    assert summary["stop_loss"] == 95.0
    assert summary["take_profit"] == 110.0
    assert summary["risk_reward"] == 2.0
    assert summary["setup_valid"] is True

    print("PASS: test_valid_trade_setup_summary")


def test_wait_trade_setup_summary():

    signal = Signal(
        market="EURUSD",
        timeframe="M5",
        direction="WAIT",
        confidence=40,
    )

    setup = TradeSetup(
        market="EURUSD",
        timeframe="M5",
        direction="WAIT",
        valid=False,
    )

    result = ScannerResult(
        market="EURUSD",
        timeframe="M5",
        candles=[make_candle()],
        analyzer=MockAnalyzer("UPTREND"),
        signal=signal,
        trade_setup=setup,
    )

    summary = result.summary()

    assert summary["signal"] == "WAIT"
    assert summary["confidence"] == 40

    assert summary["entry"] is None
    assert summary["stop_loss"] is None
    assert summary["take_profit"] is None
    assert summary["risk_reward"] is None
    assert summary["setup_valid"] is False

    print("PASS: test_wait_trade_setup_summary")


def test_missing_trade_setup_summary():

    signal = Signal(
        market="EURUSD",
        timeframe="M5",
        direction="WAIT",
        confidence=40,
    )

    result = ScannerResult(
        market="EURUSD",
        timeframe="M5",
        candles=[make_candle()],
        analyzer=MockAnalyzer("SIDEWAYS"),
        signal=signal,
        trade_setup=None,
    )

    summary = result.summary()

    assert summary["entry"] is None
    assert summary["stop_loss"] is None
    assert summary["take_profit"] is None
    assert summary["risk_reward"] is None
    assert summary["setup_valid"] is False

    print("PASS: test_missing_trade_setup_summary")


def main():

    print("=== SCANNER RESULT SUMMARY CONTRACT TEST ===")

    tests = [
        test_valid_trade_setup_summary,
        test_wait_trade_setup_summary,
        test_missing_trade_setup_summary,
    ]

    passed = 0

    for test in tests:

        try:

            test()
            passed += 1

        except AssertionError as error:

            print(
                f"FAIL: {test.__name__}"
            )

            print(
                f"      AssertionError: {error}"
            )

        except Exception as error:

            print(
                f"FAIL: {test.__name__}"
            )

            print(
                f"      {type(error).__name__}: {error}"
            )

    print()

    print(
        f"Tests passed: {passed}/{len(tests)}"
    )

    if passed != len(tests):

        raise SystemExit(1)

    print()

    print(
        "PASS: ScannerResult summary contract verified."
    )


if __name__ == "__main__":

    main()
