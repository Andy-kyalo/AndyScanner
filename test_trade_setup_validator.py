"""
test_trade_setup_validator.py

Contract tests for TradeSetupValidator.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.trade_setup import TradeSetup
from backend.trade_setup_validator import (
    TradeSetupValidator,
)


def make_setup(
    direction,
    entry=100.0,
    stop_loss=95.0,
    take_profit=110.0,
    valid=True,
):

    return TradeSetup(
        market="EURUSD",
        timeframe="M5",
        direction=direction,
        entry=entry,
        stop_loss=stop_loss,
        take_profit=take_profit,
        risk_reward=round(
            abs(take_profit - entry)
            / abs(entry - stop_loss),
            2,
        ),
        valid=valid,
    )


def test_valid_buy():

    setup = make_setup("BUY")

    result = TradeSetupValidator().validate(
        setup
    )

    assert result.valid is True
    assert result.reason == "ACCEPTED"
    assert result.risk_reward == 2.0

    print("PASS: test_valid_buy")


def test_valid_strong_buy():

    setup = make_setup("STRONG BUY")

    result = TradeSetupValidator().validate(
        setup
    )

    assert result.valid is True
    assert result.reason == "ACCEPTED"

    print("PASS: test_valid_strong_buy")


def test_valid_sell():

    setup = make_setup(
        "SELL",
        entry=100.0,
        stop_loss=105.0,
        take_profit=90.0,
    )

    result = TradeSetupValidator().validate(
        setup
    )

    assert result.valid is True
    assert result.reason == "ACCEPTED"
    assert result.risk_reward == 2.0

    print("PASS: test_valid_sell")


def test_valid_strong_sell():

    setup = make_setup(
        "STRONG SELL",
        entry=100.0,
        stop_loss=105.0,
        take_profit=90.0,
    )

    result = TradeSetupValidator().validate(
        setup
    )

    assert result.valid is True

    print("PASS: test_valid_strong_sell")


def test_low_risk_reward():

    setup = make_setup(
        "BUY",
        entry=100.0,
        stop_loss=95.0,
        take_profit=102.0,
    )

    result = TradeSetupValidator().validate(
        setup
    )

    assert result.valid is False
    assert (
        result.reason
        == "RISK_REWARD_BELOW_MINIMUM"
    )
    assert result.risk_reward == 0.4

    print("PASS: test_low_risk_reward")


def test_custom_minimum():

    setup = make_setup(
        "BUY",
        entry=100.0,
        stop_loss=95.0,
        take_profit=107.5,
    )

    result = TradeSetupValidator(
        min_risk_reward=1.5
    ).validate(setup)

    assert result.valid is True
    assert result.risk_reward == 1.5

    print("PASS: test_custom_minimum")


def test_structurally_invalid():

    setup = make_setup(
        "BUY",
        valid=False,
    )

    result = TradeSetupValidator().validate(
        setup
    )

    assert result.valid is False
    assert (
        result.reason
        == "STRUCTURALLY_INVALID"
    )

    print("PASS: test_structurally_invalid")


def test_missing_setup():

    result = TradeSetupValidator().validate(
        None
    )

    assert result.valid is False
    assert (
        result.reason
        == "TRADE_SETUP_MISSING"
    )

    print("PASS: test_missing_setup")


def test_invalid_buy_relationship():

    setup = make_setup(
        "BUY",
        entry=100.0,
        stop_loss=105.0,
        take_profit=110.0,
    )

    result = TradeSetupValidator().validate(
        setup
    )

    assert result.valid is False
    assert (
        result.reason
        == "INVALID_BUY_LEVEL_RELATIONSHIP"
    )

    print(
        "PASS: test_invalid_buy_relationship"
    )


def test_invalid_sell_relationship():

    setup = make_setup(
        "SELL",
        entry=100.0,
        stop_loss=95.0,
        take_profit=90.0,
    )

    result = TradeSetupValidator().validate(
        setup
    )

    assert result.valid is False
    assert (
        result.reason
        == "INVALID_SELL_LEVEL_RELATIONSHIP"
    )

    print(
        "PASS: test_invalid_sell_relationship"
    )


def test_zero_risk():

    setup = TradeSetup(
        market="EURUSD",
        timeframe="M5",
        direction="BUY",
        entry=100.0,
        stop_loss=100.0,
        take_profit=110.0,
        risk_reward=None,
        valid=True,
    )

    result = TradeSetupValidator().validate(setup)

    assert result.valid is False
    assert result.reason == "ZERO_RISK"

    print("PASS: test_zero_risk")


def test_zero_reward():

    setup = TradeSetup(
        market="EURUSD",
        timeframe="M5",
        direction="BUY",
        entry=100.0,
        stop_loss=95.0,
        take_profit=100.0,
        risk_reward=None,
        valid=True,
    )

    result = TradeSetupValidator().validate(setup)

    assert result.valid is False
    assert result.reason == "ZERO_REWARD"

    print("PASS: test_zero_reward")

def test_zero_reward():

    setup = make_setup(
        "BUY",
        entry=100.0,
        stop_loss=95.0,
        take_profit=100.0,
    )

    result = TradeSetupValidator().validate(
        setup
    )

    assert result.valid is False
    assert (
        result.reason
        == "STRUCTURALLY_INVALID"
    )

    print("PASS: test_zero_reward")


def test_wait_is_rejected():

    setup = TradeSetup(
        market="EURUSD",
        timeframe="M5",
        direction="WAIT",
        valid=False,
    )

    result = TradeSetupValidator().validate(
        setup
    )

    assert result.valid is False
    assert (
        result.reason
        == "STRUCTURALLY_INVALID"
    )

    print("PASS: test_wait_is_rejected")


def test_invalid_minimum():

    try:

        TradeSetupValidator(
            min_risk_reward=0
        )

    except ValueError:

        print("PASS: test_invalid_minimum")
        return

    raise AssertionError(
        "Expected ValueError."
    )


def main():

    print(
        "=== TRADE SETUP VALIDATOR CONTRACT TEST ==="
    )

    tests = [
        test_valid_buy,
        test_valid_strong_buy,
        test_valid_sell,
        test_valid_strong_sell,
        test_low_risk_reward,
        test_custom_minimum,
        test_structurally_invalid,
        test_missing_setup,
        test_invalid_buy_relationship,
        test_invalid_sell_relationship,
        test_wait_is_rejected,
        test_invalid_minimum,
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
        "PASS: Trade Setup Validator contract verified."
    )


if __name__ == "__main__":

    main()
