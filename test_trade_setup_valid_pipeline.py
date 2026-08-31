"""
test_trade_setup_valid_pipeline.py

Integration tests for valid BUY and SELL trade setups
through TradeSetupStage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.candle import Candle
from backend.analysis_result import AnalysisResult
from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.stages.trade_setup_stage import TradeSetupStage
from backend.signal import Signal


def make_candles():

    return [
        Candle(
            time="2026-08-31 13:00:00",
            open_price=96.0,
            high=98.0,
            low=95.0,
            close=97.0,
        ),
        Candle(
            time="2026-08-31 13:05:00",
            open_price=98.0,
            high=101.0,
            low=97.0,
            close=100.0,
        ),
        Candle(
            time="2026-08-31 13:10:00",
            open_price=99.0,
            high=101.0,
            low=98.0,
            close=100.0,
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

        analysis.bullish_order_block = Candle(
            time="2026-08-31 12:55:00",
            open_price=96.0,
            high=98.0,
            low=95.0,
            close=97.0,
        )

        analysis.buy_side_liquidity = [
            Candle(
                time="2026-08-31 12:50:00",
                open_price=103.0,
                high=105.0,
                low=102.0,
                close=104.0,
            )
        ]

    elif direction in ("SELL", "STRONG SELL"):

        analysis.trend = "DOWNTREND"
        analysis.bearish_bos = True

        analysis.bearish_order_block = Candle(
            time="2026-08-31 12:55:00",
            open_price=103.0,
            high=105.0,
            low=102.0,
            close=104.0,
        )

        analysis.sell_side_liquidity = [
            Candle(
                time="2026-08-31 12:50:00",
                open_price=97.0,
                high=98.0,
                low=95.0,
                close=96.0,
            )
        ]

    context.analysis = analysis

    context.signal = Signal(
        market="EURUSD",
        timeframe="M5",
        direction=direction,
        confidence=80,
    )

    return context


def test_valid_buy():

    context = make_context("BUY")

    context = TradeSetupStage().run(context)

    setup = context.trade_setup

    assert setup is not None
    assert setup.direction == "BUY"
    assert setup.entry == 100.0
    assert setup.stop_loss == 95.0
    assert setup.take_profit == 105.0
    assert setup.risk_reward == 1.0
    assert setup.valid is True

    assert context.get_metadata(
        "trade_setup"
    ) == "VALID"

    print("PASS: test_valid_buy")


def test_valid_strong_buy():

    context = make_context("STRONG BUY")

    context = TradeSetupStage().run(context)

    setup = context.trade_setup

    assert setup is not None
    assert setup.direction == "STRONG BUY"
    assert setup.entry == 100.0
    assert setup.stop_loss == 95.0
    assert setup.take_profit == 105.0
    assert setup.risk_reward == 1.0
    assert setup.valid is True

    print("PASS: test_valid_strong_buy")


def test_valid_sell():

    context = make_context("SELL")

    context = TradeSetupStage().run(context)

    setup = context.trade_setup

    assert setup is not None
    assert setup.direction == "SELL"
    assert setup.entry == 100.0
    assert setup.stop_loss == 105.0
    assert setup.take_profit == 95.0
    assert setup.risk_reward == 1.0
    assert setup.valid is True

    assert context.get_metadata(
        "trade_setup"
    ) == "VALID"

    print("PASS: test_valid_sell")


def test_valid_strong_sell():

    context = make_context("STRONG SELL")

    context = TradeSetupStage().run(context)

    setup = context.trade_setup

    assert setup is not None
    assert setup.direction == "STRONG SELL"
    assert setup.entry == 100.0
    assert setup.stop_loss == 105.0
    assert setup.take_profit == 95.0
    assert setup.risk_reward == 1.0
    assert setup.valid is True

    print("PASS: test_valid_strong_sell")


def main():

    print("=== VALID TRADE SETUP PIPELINE TEST ===")

    tests = [
        test_valid_buy,
        test_valid_strong_buy,
        test_valid_sell,
        test_valid_strong_sell,
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
        "PASS: Valid Trade Setup pipeline verified."
    )


if __name__ == "__main__":
    main()
