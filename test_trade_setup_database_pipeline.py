"""
test_trade_setup_database_pipeline.py

Integration tests for TradeSetup persistence through
the actual Database Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import os
import tempfile

from backend.candle import Candle
from backend.analysis_result import AnalysisResult
from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.stages.trade_setup_stage import TradeSetupStage
from backend.pipeline.stages.database_stage import DatabaseStage
from backend.signal import Signal
from database.database_manager import DatabaseManager


# ==========================================================
# Test Fixtures
# ==========================================================

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

    context.trend = analysis.trend

    context.signal = Signal(
        market="EURUSD",
        timeframe="M5",
        direction=direction,
        confidence=80,
    )

    return context


# ==========================================================
# Database Helpers
# ==========================================================

def run_database_stage(context, database_path):

    original_path = DatabaseManager.__init__

    def test_database_init(self, path="database/scanner.db"):

        original_path(self, database_path)

    DatabaseManager.__init__ = test_database_init

    try:

        context = DatabaseStage().run(context)

    finally:

        DatabaseManager.__init__ = original_path

    return context


def read_latest_scan(database_path):

    with DatabaseManager(database_path) as database:

        row = database.get_latest_scan()

        return dict(row) if row else None


# ==========================================================
# Valid BUY
# ==========================================================

def test_valid_buy_database_persistence():

    with tempfile.TemporaryDirectory() as directory:

        database_path = os.path.join(
            directory,
            "scanner.db",
        )

        context = make_context("BUY")

        context = TradeSetupStage().run(context)

        setup = context.trade_setup

        assert setup.valid is True
        assert setup.entry == 100.0
        assert setup.stop_loss == 95.0
        assert setup.take_profit == 105.0
        assert setup.risk_reward == 1.0

        context = run_database_stage(
            context,
            database_path,
        )

        assert context.get_metadata(
            "database"
        ) == "SAVED"

        row = read_latest_scan(database_path)

        assert row is not None

        assert row["market"] == "EURUSD"
        assert row["timeframe"] == "M5"
        assert row["signal"] == "BUY"
        assert row["confidence"] == 80

        assert row["entry"] == 100.0
        assert row["stop_loss"] == 95.0
        assert row["take_profit"] == 105.0
        assert row["risk_reward"] == 1.0
        assert row["setup_valid"] == 1

    print("PASS: test_valid_buy_database_persistence")


# ==========================================================
# Valid SELL
# ==========================================================

def test_valid_sell_database_persistence():

    with tempfile.TemporaryDirectory() as directory:

        database_path = os.path.join(
            directory,
            "scanner.db",
        )

        context = make_context("SELL")

        context = TradeSetupStage().run(context)

        setup = context.trade_setup

        assert setup.valid is True
        assert setup.entry == 100.0
        assert setup.stop_loss == 105.0
        assert setup.take_profit == 95.0
        assert setup.risk_reward == 1.0

        context = run_database_stage(
            context,
            database_path,
        )

        assert context.get_metadata(
            "database"
        ) == "SAVED"

        row = read_latest_scan(database_path)

        assert row is not None

        assert row["market"] == "EURUSD"
        assert row["timeframe"] == "M5"
        assert row["signal"] == "SELL"
        assert row["confidence"] == 80

        assert row["entry"] == 100.0
        assert row["stop_loss"] == 105.0
        assert row["take_profit"] == 95.0
        assert row["risk_reward"] == 1.0
        assert row["setup_valid"] == 1

    print("PASS: test_valid_sell_database_persistence")


# ==========================================================
# WAIT / Invalid Setup
# ==========================================================

def test_wait_database_persistence():

    with tempfile.TemporaryDirectory() as directory:

        database_path = os.path.join(
            directory,
            "scanner.db",
        )

        context = make_context("WAIT")

        context = TradeSetupStage().run(context)

        setup = context.trade_setup

        assert setup.valid is False
        assert setup.entry is None
        assert setup.stop_loss is None
        assert setup.take_profit is None
        assert setup.risk_reward is None

        context = run_database_stage(
            context,
            database_path,
        )

        assert context.get_metadata(
            "database"
        ) == "SAVED"

        row = read_latest_scan(database_path)

        assert row is not None

        assert row["market"] == "EURUSD"
        assert row["timeframe"] == "M5"
        assert row["signal"] == "WAIT"
        assert row["confidence"] == 80

        assert row["entry"] is None
        assert row["stop_loss"] is None
        assert row["take_profit"] is None
        assert row["risk_reward"] is None
        assert row["setup_valid"] == 0

    print("PASS: test_wait_database_persistence")


# ==========================================================
# Metadata
# ==========================================================

def test_trade_setup_metadata():

    with tempfile.TemporaryDirectory() as directory:

        database_path = os.path.join(
            directory,
            "scanner.db",
        )

        context = make_context("BUY")

        context = TradeSetupStage().run(context)

        context = run_database_stage(
            context,
            database_path,
        )

        assert context.get_metadata(
            "trade_setup_persisted"
        ) is True

        assert context.get_metadata(
            "trade_setup_valid"
        ) is True

    print("PASS: test_trade_setup_metadata")


# ==========================================================
# Main
# ==========================================================

def main():

    print(
        "=== TRADE SETUP DATABASE PIPELINE TEST ==="
    )

    tests = [
        test_valid_buy_database_persistence,
        test_valid_sell_database_persistence,
        test_wait_database_persistence,
        test_trade_setup_metadata,
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
        "PASS: Trade Setup database pipeline verified."
    )


if __name__ == "__main__":

    main()
