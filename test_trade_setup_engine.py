"""
test_trade_setup_engine.py

Contract tests for the AndyScanner Trade Setup Engine.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.analysis_result import AnalysisResult
from backend.candle import Candle
from backend.signal import Signal
from backend.trade_setup_engine import TradeSetupEngine


def candle(
    time,
    open_price,
    high,
    low,
    close,
):
    return Candle(
        time=time,
        open_price=open_price,
        high=high,
        low=low,
        close=close,
    )


def build_analysis():
    analysis = AnalysisResult()

    analysis.market = "EURUSD"
    analysis.timeframe = "M5"

    return analysis


def test_buy_setup():

    candles = [
        candle("10:00", 100, 102, 99, 101),
        candle("10:05", 101, 103, 100, 102),
        candle("10:10", 102, 104, 101, 103),
    ]

    analysis = build_analysis()

    analysis.bullish_order_block = candle(
        "09:55",
        100,
        101,
        98,
        99,
    )

    analysis.buy_side_liquidity = [
        candle(
            "09:50",
            105,
            110,
            104,
            109,
        )
    ]

    signal = Signal(
        market="EURUSD",
        timeframe="M5",
        direction="BUY",
        confidence=70,
    )

    setup = TradeSetupEngine(
        analysis,
        signal,
        candles,
    ).generate()

    assert setup.valid is True
    assert setup.entry == 103
    assert setup.stop_loss == 98
    assert setup.take_profit == 110
    assert setup.risk_reward == 1.4


def test_strong_buy_setup():

    candles = [
        candle("10:00", 100, 102, 99, 101),
        candle("10:05", 101, 103, 100, 102),
        candle("10:10", 102, 104, 101, 103),
    ]

    analysis = build_analysis()

    analysis.bullish_order_block = candle(
        "09:55",
        100,
        101,
        98,
        99,
    )

    analysis.buy_side_liquidity = [
        candle(
            "09:50",
            105,
            110,
            104,
            109,
        )
    ]

    signal = Signal(
        market="EURUSD",
        timeframe="M5",
        direction="STRONG BUY",
        confidence=80,
    )

    setup = TradeSetupEngine(
        analysis,
        signal,
        candles,
    ).generate()

    assert setup.valid is True
    assert setup.direction == "STRONG BUY"
    assert setup.entry == 103
    assert setup.stop_loss == 98
    assert setup.take_profit == 110


def test_sell_setup():

    candles = [
        candle("10:00", 100, 101, 98, 99),
        candle("10:05", 99, 100, 97, 98),
        candle("10:10", 98, 99, 96, 97),
    ]

    analysis = build_analysis()

    analysis.bearish_order_block = candle(
        "09:55",
        103,
        105,
        102,
        104,
    )

    analysis.sell_side_liquidity = [
        candle(
            "09:50",
            95,
            96,
            90,
            91,
        )
    ]

    signal = Signal(
        market="EURUSD",
        timeframe="M5",
        direction="SELL",
        confidence=70,
    )

    setup = TradeSetupEngine(
        analysis,
        signal,
        candles,
    ).generate()

    assert setup.valid is True
    assert setup.entry == 97
    assert setup.stop_loss == 105
    assert setup.take_profit == 90
    assert setup.risk_reward == 0.88


def test_strong_sell_setup():

    candles = [
        candle("10:00", 100, 101, 98, 99),
        candle("10:05", 99, 100, 97, 98),
        candle("10:10", 98, 99, 96, 97),
    ]

    analysis = build_analysis()

    analysis.bearish_order_block = candle(
        "09:55",
        103,
        105,
        102,
        104,
    )

    analysis.sell_side_liquidity = [
        candle(
            "09:50",
            95,
            96,
            90,
            91,
        )
    ]

    signal = Signal(
        market="EURUSD",
        timeframe="M5",
        direction="STRONG SELL",
        confidence=80,
    )

    setup = TradeSetupEngine(
        analysis,
        signal,
        candles,
    ).generate()

    assert setup.valid is True
    assert setup.direction == "STRONG SELL"
    assert setup.entry == 97
    assert setup.stop_loss == 105
    assert setup.take_profit == 90


def test_wait_produces_invalid_setup():

    candles = [
        candle("10:00", 100, 102, 99, 101),
        candle("10:05", 101, 103, 100, 102),
        candle("10:10", 102, 104, 101, 103),
    ]

    analysis = build_analysis()

    signal = Signal(
        market="EURUSD",
        timeframe="M5",
        direction="WAIT",
        confidence=40,
    )

    setup = TradeSetupEngine(
        analysis,
        signal,
        candles,
    ).generate()

    assert setup.valid is False
    assert setup.entry is None
    assert setup.stop_loss is None
    assert setup.take_profit is None
    assert setup.risk_reward is None


def test_buy_without_order_block_is_invalid():

    candles = [
        candle("10:00", 100, 102, 99, 101),
        candle("10:05", 101, 103, 100, 102),
        candle("10:10", 102, 104, 101, 103),
    ]

    analysis = build_analysis()

    analysis.buy_side_liquidity = [
        candle(
            "09:50",
            105,
            110,
            104,
            109,
        )
    ]

    signal = Signal(
        market="EURUSD",
        timeframe="M5",
        direction="BUY",
        confidence=70,
    )

    setup = TradeSetupEngine(
        analysis,
        signal,
        candles,
    ).generate()

    assert setup.valid is False
    assert setup.stop_loss is None
    assert setup.take_profit == 110
    assert setup.risk_reward is None


def test_sell_without_order_block_is_invalid():

    candles = [
        candle("10:00", 100, 101, 98, 99),
        candle("10:05", 99, 100, 97, 98),
        candle("10:10", 98, 99, 96, 97),
    ]

    analysis = build_analysis()

    analysis.sell_side_liquidity = [
        candle(
            "09:50",
            95,
            96,
            90,
            91,
        )
    ]

    signal = Signal(
        market="EURUSD",
        timeframe="M5",
        direction="SELL",
        confidence=70,
    )

    setup = TradeSetupEngine(
        analysis,
        signal,
        candles,
    ).generate()

    assert setup.valid is False
    assert setup.stop_loss is None
    assert setup.take_profit == 90
    assert setup.risk_reward is None


def test_buy_without_target_is_invalid():

    candles = [
        candle("10:00", 100, 102, 99, 101),
        candle("10:05", 101, 103, 100, 102),
        candle("10:10", 102, 104, 101, 103),
    ]

    analysis = build_analysis()

    analysis.bullish_order_block = candle(
        "09:55",
        100,
        101,
        98,
        99,
    )

    signal = Signal(
        market="EURUSD",
        timeframe="M5",
        direction="BUY",
        confidence=70,
    )

    setup = TradeSetupEngine(
        analysis,
        signal,
        candles,
    ).generate()

    assert setup.valid is False
    assert setup.entry == 103
    assert setup.stop_loss == 98
    assert setup.take_profit is None
    assert setup.risk_reward is None


def test_sell_without_target_is_invalid():

    candles = [
        candle("10:00", 100, 101, 98, 99),
        candle("10:05", 99, 100, 97, 98),
        candle("10:10", 98, 99, 96, 97),
    ]

    analysis = build_analysis()

    analysis.bearish_order_block = candle(
        "09:55",
        103,
        105,
        102,
        104,
    )

    signal = Signal(
        market="EURUSD",
        timeframe="M5",
        direction="SELL",
        confidence=70,
    )

    setup = TradeSetupEngine(
        analysis,
        signal,
        candles,
    ).generate()

    assert setup.valid is False
    assert setup.entry == 97
    assert setup.stop_loss == 105
    assert setup.take_profit is None
    assert setup.risk_reward is None


def test_buy_invalid_level_relationship():

    candles = [
        candle("10:00", 100, 102, 99, 101),
        candle("10:05", 101, 103, 100, 102),
        candle("10:10", 102, 104, 101, 103),
    ]

    analysis = build_analysis()

    analysis.bullish_order_block = candle(
        "09:55",
        105,
        106,
        104,
        105,
    )

    analysis.buy_side_liquidity = [
        candle(
            "09:50",
            105,
            110,
            104,
            109,
        )
    ]

    signal = Signal(
        market="EURUSD",
        timeframe="M5",
        direction="BUY",
        confidence=70,
    )

    setup = TradeSetupEngine(
        analysis,
        signal,
        candles,
    ).generate()

    assert setup.valid is False
    assert setup.risk_reward is None


def test_sell_invalid_level_relationship():

    candles = [
        candle("10:00", 100, 101, 98, 99),
        candle("10:05", 99, 100, 97, 98),
        candle("10:10", 98, 99, 96, 97),
    ]

    analysis = build_analysis()

    analysis.bearish_order_block = candle(
        "09:55",
        95,
        96,
        94,
        95,
    )

    analysis.sell_side_liquidity = [
        candle(
            "09:50",
            90,
            91,
            85,
            86,
        )
    ]

    signal = Signal(
        market="EURUSD",
        timeframe="M5",
        direction="SELL",
        confidence=70,
    )

    setup = TradeSetupEngine(
        analysis,
        signal,
        candles,
    ).generate()

    assert setup.valid is False
    assert setup.risk_reward is None


print("=== TRADE SETUP ENGINE CONTRACT TEST ===")

tests = [
    test_buy_setup,
    test_strong_buy_setup,
    test_sell_setup,
    test_strong_sell_setup,
    test_wait_produces_invalid_setup,
    test_buy_without_order_block_is_invalid,
    test_sell_without_order_block_is_invalid,
    test_buy_without_target_is_invalid,
    test_sell_without_target_is_invalid,
    test_buy_invalid_level_relationship,
    test_sell_invalid_level_relationship,
]

passed = 0

for test in tests:

    try:

        test()

        print(f"PASS: {test.__name__}")

        passed += 1

    except Exception as error:

        print(f"FAIL: {test.__name__}")
        print(f"      {type(error).__name__}: {error}")


print()
print(f"Tests passed: {passed}/{len(tests)}")

if passed != len(tests):
    raise SystemExit(1)

print()
print("PASS: Trade Setup Engine contract verified.")
