"""
test_decision_engine.py

Contract tests for the Andy Scanner Decision Engine.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.decision_engine import DecisionEngine
from backend.signal import Signal
from backend.trade_setup import TradeSetup
from backend.trade_setup_validator import (
    TradeSetupValidationResult,
)


def make_signal(direction, confidence=80):

    return Signal(
        market="EURUSD",
        timeframe="M5",
        direction=direction,
        confidence=confidence,
    )


def make_setup(
    direction,
    valid=True,
    entry=100.0,
    stop_loss=95.0,
    take_profit=110.0,
):

    return TradeSetup(
        market="EURUSD",
        timeframe="M5",
        direction=direction,
        entry=entry,
        stop_loss=stop_loss,
        take_profit=take_profit,
        risk_reward=2.0,
        valid=valid,
    )


def make_validation(
    valid=True,
    reason="ACCEPTED",
    risk_reward=2.0,
):

    return TradeSetupValidationResult(
        valid=valid,
        reason=reason,
        risk_reward=risk_reward,
    )


# ==========================================================
# BUY
# ==========================================================

def test_buy_accepted():

    signal = make_signal("BUY")

    setup = make_setup("BUY")

    validation = make_validation()

    decision = DecisionEngine().generate(
        signal,
        setup,
        validation,
    )

    assert decision.direction == "BUY"
    assert decision.signal_direction == "BUY"
    assert decision.setup_valid is True
    assert decision.risk_valid is True
    assert decision.risk_reward == 2.0
    assert decision.reason == "ACCEPTED"

    print("PASS: test_buy_accepted")


# ==========================================================
# STRONG BUY
# ==========================================================

def test_strong_buy_accepted():

    signal = make_signal(
        "STRONG BUY",
        confidence=80,
    )

    setup = make_setup(
        "STRONG BUY"
    )

    validation = make_validation()

    decision = DecisionEngine().generate(
        signal,
        setup,
        validation,
    )

    assert decision.direction == "STRONG BUY"
    assert decision.signal_direction == "STRONG BUY"
    assert decision.confidence == 80
    assert decision.setup_valid is True
    assert decision.risk_valid is True
    assert decision.reason == "ACCEPTED"

    print("PASS: test_strong_buy_accepted")


# ==========================================================
# SELL
# ==========================================================

def test_sell_accepted():

    signal = make_signal("SELL")

    setup = make_setup(
        "SELL",
        entry=100.0,
        stop_loss=105.0,
        take_profit=90.0,
    )

    validation = make_validation(
        risk_reward=2.0
    )

    decision = DecisionEngine().generate(
        signal,
        setup,
        validation,
    )

    assert decision.direction == "SELL"
    assert decision.signal_direction == "SELL"
    assert decision.setup_valid is True
    assert decision.risk_valid is True
    assert decision.reason == "ACCEPTED"

    print("PASS: test_sell_accepted")


# ==========================================================
# STRONG SELL
# ==========================================================

def test_strong_sell_accepted():

    signal = make_signal(
        "STRONG SELL",
        confidence=80,
    )

    setup = make_setup(
        "STRONG SELL",
        entry=100.0,
        stop_loss=105.0,
        take_profit=90.0,
    )

    validation = make_validation()

    decision = DecisionEngine().generate(
        signal,
        setup,
        validation,
    )

    assert decision.direction == "STRONG SELL"
    assert decision.signal_direction == "STRONG SELL"
    assert decision.confidence == 80
    assert decision.setup_valid is True
    assert decision.risk_valid is True
    assert decision.reason == "ACCEPTED"

    print("PASS: test_strong_sell_accepted")


# ==========================================================
# LOW RISK/REWARD
# ==========================================================

def test_low_rr_rejected():

    signal = make_signal("BUY")

    setup = make_setup(
        "BUY",
        valid=True,
    )

    validation = make_validation(
        valid=False,
        reason="RISK_REWARD_BELOW_MINIMUM",
        risk_reward=0.4,
    )

    decision = DecisionEngine().generate(
        signal,
        setup,
        validation,
    )

    assert decision.direction == "WAIT"
    assert decision.signal_direction == "BUY"
    assert decision.setup_valid is True
    assert decision.risk_valid is False
    assert decision.risk_reward == 0.4
    assert decision.reason == (
        "RISK_REWARD_BELOW_MINIMUM"
    )

    print("PASS: test_low_rr_rejected")


# ==========================================================
# STRUCTURALLY INVALID
# ==========================================================

def test_structurally_invalid():

    signal = make_signal("BUY")

    setup = make_setup(
        "BUY",
        valid=False,
    )

    validation = make_validation(
        valid=False,
        reason="STRUCTURALLY_INVALID",
        risk_reward=None,
    )

    decision = DecisionEngine().generate(
        signal,
        setup,
        validation,
    )

    assert decision.direction == "WAIT"
    assert decision.signal_direction == "BUY"
    assert decision.setup_valid is False
    assert decision.risk_valid is False
    assert decision.reason == (
        "STRUCTURALLY_INVALID"
    )

    print("PASS: test_structurally_invalid")


# ==========================================================
# WAIT
# ==========================================================

def test_wait():

    signal = make_signal(
        "WAIT",
        confidence=40,
    )

    setup = make_setup(
        "WAIT",
        valid=False,
    )

    validation = make_validation(
        valid=False,
        reason="STRUCTURALLY_INVALID",
        risk_reward=None,
    )

    decision = DecisionEngine().generate(
        signal,
        setup,
        validation,
    )

    assert decision.direction == "WAIT"
    assert decision.signal_direction == "WAIT"
    assert decision.confidence == 40
    assert decision.setup_valid is False
    assert decision.risk_valid is False
    assert decision.reason == (
        "STRUCTURALLY_INVALID"
    )

    print("PASS: test_wait")


# ==========================================================
# MISSING SETUP
# ==========================================================

def test_missing_setup():

    signal = make_signal("BUY")

    validation = make_validation(
        valid=False,
        reason="TRADE_SETUP_MISSING",
        risk_reward=None,
    )

    decision = DecisionEngine().generate(
        signal,
        None,
        validation,
    )

    assert decision.direction == "WAIT"
    assert decision.signal_direction == "BUY"
    assert decision.setup_valid is False
    assert decision.risk_valid is False
    assert decision.reason == (
        "TRADE_SETUP_MISSING"
    )

    print("PASS: test_missing_setup")


# ==========================================================
# MISSING VALIDATION
# ==========================================================

def test_missing_validation():

    signal = make_signal("BUY")

    setup = make_setup("BUY")

    decision = DecisionEngine().generate(
        signal,
        setup,
        None,
    )

    assert decision.direction == "WAIT"
    assert decision.signal_direction == "BUY"
    assert decision.setup_valid is False
    assert decision.risk_valid is False
    assert decision.reason == (
        "RISK_VALIDATION_MISSING"
    )

    print("PASS: test_missing_validation")


# ==========================================================
# MISSING SIGNAL
# ==========================================================

def test_missing_signal():

    decision = DecisionEngine().generate(
        None,
        None,
        None,
    )

    assert decision.direction == "WAIT"
    assert decision.signal_direction is None
    assert decision.confidence == 0
    assert decision.reason == "SIGNAL_MISSING"

    print("PASS: test_missing_signal")


# ==========================================================
# SUMMARY
# ==========================================================

def test_decision_summary():

    signal = make_signal(
        "STRONG BUY",
        confidence=85,
    )

    setup = make_setup(
        "STRONG BUY"
    )

    validation = make_validation(
        valid=True,
        reason="ACCEPTED",
        risk_reward=2.0,
    )

    decision = DecisionEngine().generate(
        signal,
        setup,
        validation,
    )

    summary = decision.summary()

    assert summary["market"] == "EURUSD"
    assert summary["timeframe"] == "M5"
    assert summary["direction"] == "STRONG BUY"
    assert summary["confidence"] == 85
    assert summary["signal_direction"] == "STRONG BUY"
    assert summary["setup_valid"] is True
    assert summary["risk_valid"] is True
    assert summary["risk_reward"] == 2.0
    assert summary["reason"] == "ACCEPTED"

    print("PASS: test_decision_summary")


# ==========================================================
# MAIN
# ==========================================================

def main():

    print(
        "=== DECISION ENGINE CONTRACT TEST ==="
    )

    tests = [
        test_buy_accepted,
        test_strong_buy_accepted,
        test_sell_accepted,
        test_strong_sell_accepted,
        test_low_rr_rejected,
        test_structurally_invalid,
        test_wait,
        test_missing_setup,
        test_missing_validation,
        test_missing_signal,
        test_decision_summary,
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
        "PASS: Decision Engine contract verified."
    )


if __name__ == "__main__":

    main()
