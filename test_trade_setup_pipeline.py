"""
test_trade_setup_pipeline.py

Integration tests for the TradeSetupStage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.stages.trade_setup_stage import TradeSetupStage
from backend.analysis_result import AnalysisResult
from backend.signal import Signal
from backend.candle import Candle


def make_candles():

    return [
        Candle(
            time="2026-08-31 13:00:00",
            open_price=100.0,
            high=105.0,
            low=99.0,
            close=104.0,
        ),
        Candle(
            time="2026-08-31 13:05:00",
            open_price=104.0,
            high=110.0,
            low=103.0,
            close=109.0,
        ),
        Candle(
            time="2026-08-31 13:10:00",
            open_price=109.0,
            high=112.0,
            low=108.0,
            close=111.0,
        ),
    ]


def make_context(direction):

    context = PipelineContext()

    context.start(
        "EURUSD",
        "M5",
    )

    context.candles = make_candles()

    analysis = AnalysisResult()

    analysis.market = "EURUSD"
    analysis.timeframe = "M5"

    if direction in ("BUY", "STRONG BUY"):

        analysis.trend = "UPTREND"

        analysis.bullish_bos = True

        analysis.bullish_order_block = (
            context.candles[0]
        )

        analysis.bullish_fvg = [
            {
                "type": "BULLISH",
                "gap_top": 108.0,
                "gap_bottom": 106.0,
                "gap_size": 2.0,
            }
        ]

    elif direction in ("SELL", "STRONG SELL"):

        analysis.trend = "DOWNTREND"

        analysis.bearish_bos = True

        analysis.bearish_order_block = (
            context.candles[0]
        )

        analysis.bearish_fvg = [
            {
                "type": "BEARISH",
                "gap_top": 106.0,
                "gap_bottom": 104.0,
                "gap_size": 2.0,
            }
        ]

    context.analysis = analysis

    context.signal = Signal(
        market="EURUSD",
        timeframe="M5",
        direction=direction,
        confidence=80,
    )

    return context


def test_buy_stage():

    context = make_context("BUY")

    result = TradeSetupStage().execute(context)

    assert result.trade_setup is not None
    assert result.trade_setup.direction == "BUY"
    assert result.trade_setup.market == "EURUSD"
    assert result.trade_setup.timeframe == "M5"

    print("PASS: test_buy_stage")


def test_sell_stage():

    context = make_context("SELL")

    result = TradeSetupStage().execute(context)

    assert result.trade_setup is not None
    assert result.trade_setup.direction == "SELL"
    assert result.trade_setup.market == "EURUSD"
    assert result.trade_setup.timeframe == "M5"

    print("PASS: test_sell_stage")


def test_wait_stage():

    context = make_context("WAIT")

    result = TradeSetupStage().execute(context)

    assert result.trade_setup is not None
    assert result.trade_setup.direction == "WAIT"
    assert result.trade_setup.valid is False

    print("PASS: test_wait_stage")


def main():

    print("=== TRADE SETUP PIPELINE INTEGRATION TEST ===")

    tests = [
        test_buy_stage,
        test_sell_stage,
        test_wait_stage,
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
        "PASS: Trade Setup Stage integration verified."
    )


if __name__ == "__main__":

    main()