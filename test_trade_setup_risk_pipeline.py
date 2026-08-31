"""
test_trade_setup_risk_pipeline.py

Integration tests for Trade Setup risk/quality
validation inside the pipeline stage.

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


def make_context(
    direction,
    take_profit=105.0,
):

    context = PipelineContext()

    context.start(
        "EURUSD",
        "M5",
    )

    context.candles = make_candles()

    analysis = AnalysisResult()

    analysis.market = "EURUSD"
    analysis.timeframe = "M5"

    if direction in (
        "BUY",
        "STRONG BUY",
    ):

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
                open_price=take_profit - 1.0,
                high=take_profit,
                low=take_profit - 2.0,
                close=take_profit - 0.5,
    )
]

    elif direction in (
        "SELL",
        "STRONG SELL",
    ):

        analysis.trend = "DOWNTREND"
        analysis.bearish_bos = True

        analysis.bearish_order_block = Candle(
            time="2026-08-31 12:55:00",
            open_price=103.0,
            high=105.0,
            low=102.0,
            close=104.0,
        )

        # The low must be <= both open and close.
        # For take_profit=90.0, close=90.0,
        # therefore low must be <= 90.0.
        analysis.sell_side_liquidity = [
            Candle(
                time="2026-08-31 12:50:00",
                open_price=take_profit + 1.0,
                high=take_profit + 2.0,
                low=take_profit,
               close=take_profit + 0.5,
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


def test_acceptable_buy():

    context = make_context(
        "BUY",
        take_profit=110.0,
    )

    context = TradeSetupStage().run(
        context
    )

    validation = context.trade_setup_validation

    assert validation is not None
    assert validation.valid is True
    assert validation.reason == "ACCEPTED"
    assert validation.risk_reward == 2.0

    assert context.get_metadata(
        "risk_validation"
    ) == "ACCEPTED"

    assert context.get_metadata(
        "risk_validation_reason"
    ) == "ACCEPTED"

    print("PASS: test_acceptable_buy")


def test_low_rr_buy_rejected():

    context = make_context(
        "BUY",
        take_profit=102.0,
    )

    context = TradeSetupStage().run(
        context
    )

    setup = context.trade_setup
    validation = context.trade_setup_validation

    assert setup.valid is True

    assert validation.valid is False

    assert (
        validation.reason
        == "RISK_REWARD_BELOW_MINIMUM"
    )

    assert validation.risk_reward == 0.4

    assert context.get_metadata(
        "risk_validation"
    ) == "REJECTED"

    assert context.get_metadata(
        "risk_validation_reason"
    ) == "RISK_REWARD_BELOW_MINIMUM"

    print("PASS: test_low_rr_buy_rejected")


def test_acceptable_sell():

    context = make_context(
        "SELL",
        take_profit=90.0,
    )

    context = TradeSetupStage().run(
        context
    )

    validation = context.trade_setup_validation

    assert validation is not None
    assert validation.valid is True
    assert validation.reason == "ACCEPTED"
    assert validation.risk_reward == 2.0

    print("PASS: test_acceptable_sell")


def test_low_rr_sell_rejected():

    context = make_context(
        "SELL",
        take_profit=98.0,
    )

    context = TradeSetupStage().run(
        context
    )

    setup = context.trade_setup
    validation = context.trade_setup_validation

    assert setup.valid is True

    assert validation.valid is False

    assert (
        validation.reason
        == "RISK_REWARD_BELOW_MINIMUM"
    )

    assert validation.risk_reward == 0.4

    print("PASS: test_low_rr_sell_rejected")


def test_wait_rejected():

    context = make_context(
        "WAIT"
    )

    context = TradeSetupStage().run(
        context
    )

    setup = context.trade_setup
    validation = context.trade_setup_validation

    assert setup.valid is False
    assert validation.valid is False

    assert (
        validation.reason
        == "STRUCTURALLY_INVALID"
    )

    assert context.get_metadata(
        "risk_validation"
    ) == "REJECTED"

    print("PASS: test_wait_rejected")


def test_custom_rr_threshold():

    context = make_context(
        "BUY",
        take_profit=107.5,
    )

    context = TradeSetupStage(
        min_risk_reward=1.5
    ).run(context)

    validation = context.trade_setup_validation

    assert validation.valid is True
    assert validation.risk_reward == 1.5

    print("PASS: test_custom_rr_threshold")


def main():

    print(
        "=== TRADE SETUP RISK PIPELINE TEST ==="
    )

    tests = [
        test_acceptable_buy,
        test_low_rr_buy_rejected,
        test_acceptable_sell,
        test_low_rr_sell_rejected,
        test_wait_rejected,
        test_custom_rr_threshold,
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
        f"Tests passed: "
        f"{passed}/{len(tests)}"
    )

    if passed != len(tests):

        raise SystemExit(1)

    print()
    print(
        "PASS: Trade Setup Risk pipeline verified."
    )


if __name__ == "__main__":
    main()