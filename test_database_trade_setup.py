"""
test_database_trade_setup.py

Contract tests for TradeSetup database persistence.
"""

import os
import sqlite3
import tempfile

from database.database_manager import DatabaseManager
from backend.trade_setup import TradeSetup


def test_valid_buy_setup():

    with tempfile.TemporaryDirectory() as directory:

        database_path = os.path.join(
            directory,
            "test.db",
        )

        setup = TradeSetup(
            market="EURUSD",
            timeframe="M5",
            direction="BUY",
            entry=1.1000,
            stop_loss=1.0950,
            take_profit=1.1100,
            risk_reward=2.0,
            valid=True,
        )

        with DatabaseManager(database_path) as database:

            database.save_scan(
                market="EURUSD",
                timeframe="M5",
                trend="UPTREND",
                signal="BUY",
                confidence=70,
                trade_setup=setup,
            )

            row = database.get_latest_scan()

            assert row["market"] == "EURUSD"
            assert row["timeframe"] == "M5"
            assert row["signal"] == "BUY"
            assert row["confidence"] == 70

            assert row["entry"] == 1.1000
            assert row["stop_loss"] == 1.0950
            assert row["take_profit"] == 1.1100
            assert row["risk_reward"] == 2.0
            assert row["setup_valid"] == 1


def test_valid_sell_setup():

    with tempfile.TemporaryDirectory() as directory:

        database_path = os.path.join(
            directory,
            "test.db",
        )

        setup = TradeSetup(
            market="GBPUSD",
            timeframe="M5",
            direction="SELL",
            entry=1.3000,
            stop_loss=1.3050,
            take_profit=1.2900,
            risk_reward=2.0,
            valid=True,
        )

        with DatabaseManager(database_path) as database:

            database.save_scan(
                market="GBPUSD",
                timeframe="M5",
                trend="DOWNTREND",
                signal="SELL",
                confidence=75,
                trade_setup=setup,
            )

            row = database.get_latest_scan()

            assert row["entry"] == 1.3000
            assert row["stop_loss"] == 1.3050
            assert row["take_profit"] == 1.2900
            assert row["risk_reward"] == 2.0
            assert row["setup_valid"] == 1


def test_wait_setup():

    with tempfile.TemporaryDirectory() as directory:

        database_path = os.path.join(
            directory,
            "test.db",
        )

        setup = TradeSetup(
            market="USDJPY",
            timeframe="M5",
            direction="WAIT",
            valid=False,
        )

        with DatabaseManager(database_path) as database:

            database.save_scan(
                market="USDJPY",
                timeframe="M5",
                trend="UPTREND",
                signal="WAIT",
                confidence=40,
                trade_setup=setup,
            )

            row = database.get_latest_scan()

            assert row["signal"] == "WAIT"
            assert row["entry"] is None
            assert row["stop_loss"] is None
            assert row["take_profit"] is None
            assert row["risk_reward"] is None
            assert row["setup_valid"] == 0


def test_backward_compatible_save():

    with tempfile.TemporaryDirectory() as directory:

        database_path = os.path.join(
            directory,
            "test.db",
        )

        with DatabaseManager(database_path) as database:

            database.save_scan(
                market="XAUUSD",
                timeframe="M5",
                trend="UPTREND",
                signal="WAIT",
                confidence=40,
            )

            row = database.get_latest_scan()

            assert row["market"] == "XAUUSD"
            assert row["entry"] is None
            assert row["stop_loss"] is None
            assert row["take_profit"] is None
            assert row["risk_reward"] is None
            assert row["setup_valid"] == 0


def test_limit_parameter():

    with tempfile.TemporaryDirectory() as directory:

        database_path = os.path.join(
            directory,
            "test.db",
        )

        with DatabaseManager(database_path) as database:

            for index in range(5):

                database.save_scan(
                    market=f"TEST{index}",
                    timeframe="M5",
                    trend="UPTREND",
                    signal="WAIT",
                    confidence=40,
                )

            rows = database.get_all_scans(limit=3)

            assert len(rows) == 3


def run_tests():

    tests = [
        test_valid_buy_setup,
        test_valid_sell_setup,
        test_wait_setup,
        test_backward_compatible_save,
        test_limit_parameter,
    ]

    passed = 0

    for test in tests:

        try:

            test()
            print(
                f"PASS: {test.__name__}"
            )
            passed += 1

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
        "PASS: Trade Setup database persistence verified."
    )


if __name__ == "__main__":
    run_tests()
