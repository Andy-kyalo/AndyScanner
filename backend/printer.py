"""
printer.py

Professional reporting system for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""

from backend.signal_engine import SignalEngine


# ==========================================================
# Report Formatting Configuration
# ==========================================================

DEFAULT_WIDTH = 60

TITLE_CHAR = "="
DIVIDER_CHAR = "-"
EMPTY_VALUE = "None"


# ==========================================================
# Internal Formatting Helpers
# ==========================================================

def _width(title: str) -> int:
    """
    Determine report width.
    """
    return max(DEFAULT_WIDTH, len(title) + 20)


def _section(title: str):
    """
    Print section header.
    """

    width = _width(title)

    print()
    print(TITLE_CHAR * width)
    print(title.center(width))
    print(TITLE_CHAR * width)


def _footer(title: str):
    """
    Print section footer.
    """

    print(TITLE_CHAR * _width(title))
    print()


def _divider():
    """
    Print divider.
    """

    print(DIVIDER_CHAR * DEFAULT_WIDTH)


def _line(label: str, value):
    """
    Print aligned key/value pair.
    """

    print(f"{label:<20}: {value}")


def _status(name: str, passed: bool):
    """
    Print YES / NO status.
    """

    value = "YES" if passed else "NO"

    print(f"{name:<20}: {value}")


def _empty(message="No data available."):
    """
    Print empty message.
    """

    print(message)


def _collection(title, items, formatter):
    """
    Generic collection printer.
    """

    _section(title)

    if not items:

        _empty()

    else:

        for item in items:

            formatter(item)

    _footer(title)


def _print_candle(candle):
    """
    Print one candle.
    """

    _line("Time", candle.time)
    _line("Open", candle.open)
    _line("High", candle.high)
    _line("Low", candle.low)
    _line("Close", candle.close)

    if hasattr(candle, "candle_type"):
        _line("Type", candle.candle_type())
    elif hasattr(candle, "type"):
        _line("Type", candle.type)
    elif hasattr(candle, "is_bullish"):

        if callable(candle.is_bullish):
            candle_type = "Bullish" if candle.is_bullish() else "Bearish"
        else:
            candle_type = "Bullish" if candle.is_bullish else "Bearish"

        _line("Type", candle_type)
    else:
        _line("Type", "Unknown")
# Analysis Report
# ==========================================================

def print_analysis(analyzer):
    """
    Print overall market analysis.
    """

    _section("Analysis")

    _line("Total Candles", len(analyzer.candles))
    _line("Highest High", analyzer.highest_high())
    _line("Lowest Low", analyzer.lowest_low())
    _line("Trend", analyzer.trend())

    _footer("Analysis")


# ==========================================================
# Strongest Candle Report
# ==========================================================

def print_strongest_candle(analyzer):
    """
    Print strongest candle.
    """

    strongest = analyzer.strongest_candle()

    _section("Strongest Candle")

    if strongest is None:

        _empty("No strongest candle found.")

    else:

        _line("Time", strongest.time)
        _line("Open", strongest.open)
        _line("High", strongest.high)
        _line("Low", strongest.low)
        _line("Close", strongest.close)

        _line("Body Size", strongest.body_size())
        _line("Range", strongest.range())

    _footer("Strongest Candle")


# ==========================================================
# Market Structure Report
# ==========================================================

def print_market_structure(analyzer):
    """
    Print market structure.
    """

    _section("Market Structure")

    structure = "No Break of Structure"

    if analyzer.bullish_bos():
        structure = "Bullish BOS"

    elif analyzer.bearish_bos():
        structure = "Bearish BOS"

    _line("Trend", analyzer.trend())
    _line("Highest High", analyzer.highest_high())
    _line("Lowest Low", analyzer.lowest_low())
    _line("Structure", structure)

    _footer("Market Structure")
    
    
    # ==========================================================
# Engulfing Patterns Report
# ==========================================================

def print_engulfing(analyzer):
    """
    Print bullish and bearish engulfing patterns.
    """

    _section("Engulfing Patterns")

    bullish = analyzer.bullish_engulfing()
    bearish = analyzer.bearish_engulfing()

    found = False

    if bullish:

        found = True

        print("Bullish Engulfing")
        _divider()

        for candle in bullish:

            _line("Time", candle.time)
            _line("Open", candle.open)
            _line("High", candle.high)
            _line("Low", candle.low)
            _line("Close", candle.close)

            _divider()

    if bearish:

        found = True

        print("Bearish Engulfing")
        _divider()

        for candle in bearish:

            _line("Time", candle.time)
            _line("Open", candle.open)
            _line("High", candle.high)
            _line("Low", candle.low)
            _line("Close", candle.close)

            _divider()

    if not found:

        _empty("No Engulfing Pattern.")

    _footer("Engulfing Patterns")
    
    # ==========================================================
# Swing Highs Report
# ==========================================================

def print_swing_highs(analyzer):
    """
    Print detected swing highs.
    """

    swings = analyzer.swing_highs()

    _section("Swing Highs")

    if not swings:

        _empty("No Swing High found.")

    else:

        for candle in swings:

            _line("Time", candle.time)
            _line("High", candle.high)
            _divider()

    _footer("Swing Highs")


# ==========================================================
# Swing Lows Report
# ==========================================================

def print_swing_lows(analyzer):
    """
    Print detected swing lows.
    """

    swings = analyzer.swing_lows()

    _section("Swing Lows")

    if not swings:

        _empty("No Swing Low found.")

    else:

        for candle in swings:

            _line("Time", candle.time)
            _line("Low", candle.low)
            _divider()

    _footer("Swing Lows")


# ==========================================================
# Break Of Structure Report
# ==========================================================

def print_bos(analyzer):
    """
    Print Break Of Structure.
    """

    _section("Break Of Structure")

    _status("Bullish BOS", analyzer.bullish_bos())
    _status("Bearish BOS", analyzer.bearish_bos())

    _footer("Break Of Structure")


# ==========================================================
# Change Of Character Report
# ==========================================================

def print_choch(analyzer):
    """
    Print Change Of Character.
    """

    _section("Change Of Character")

    if analyzer.bullish_choch():

        _line("Direction", "Bullish")

    elif analyzer.bearish_choch():

        _line("Direction", "Bearish")

    else:

        _empty("No Change Of Character.")

    _footer("Change Of Character")
    
    # ==========================================================
# Order Blocks Report
# ==========================================================

def print_order_blocks(analyzer):
    """
    Print Bullish Order Blocks.
    """

    _section("Bullish Order Block")

    order_block = analyzer.bullish_order_block()

    if order_block is None:

        _empty("No Bullish Order Block.")

    else:

        _line("Time", order_block.time)
        _line("Open", order_block.open)
        _line("High", order_block.high)
        _line("Low", order_block.low)
        _line("Close", order_block.close)

    _footer("Bullish Order Block")


# ==========================================================
# Fair Value Gap Report
# ==========================================================

def print_fvg(analyzer):
    """
    Print Bullish Fair Value Gaps.
    """

    _section("Bullish Fair Value Gap")

    fvgs = analyzer.bullish_fvg()

    if not fvgs:

        _empty("No Bullish FVG.")

    else:

        for index, gap in enumerate(fvgs, start=1):

            first = gap["first"]
            third = gap["third"]

            _line("Gap", index)
            _line("From", first.time)
            _line("To", third.time)
            _line("Upper", first.high)
            _line("Lower", third.low)
            _line("Gap Size", gap["gap_size"])

            if index != len(fvgs):
                _divider()

    _footer("Bullish Fair Value Gap")


# ==========================================================
# Liquidity Report
# ==========================================================

def print_liquidity(analyzer):
    """
    Print liquidity zones.
    """

    _section("Liquidity")

    buy = analyzer.buy_side_liquidity()
    sell = analyzer.sell_side_liquidity()

    print("BUY-SIDE LIQUIDITY")
    _divider()

    if not buy:

        _empty("None")

    else:

        for candle in buy:

            _line("Time", candle.time)
            _line("High", candle.high)
            _divider()

    print()

    print("SELL-SIDE LIQUIDITY")
    _divider()

    if not sell:

        _empty("None")

    else:

        for candle in sell:

            _line("Time", candle.time)
            _line("Low", candle.low)
            _divider()

    _footer("Liquidity")
    
    # ==========================================================
# Trading Signal Report
# ==========================================================

def print_signal(analyzer):
    """
    Print generated trading signal.
    """

    signal_engine = SignalEngine(analyzer)
    signal = signal_engine.generate()

    _section("Trading Signal")

    _line("Market", signal.market)
    _line("Timeframe", signal.timeframe)
    _line("Direction", signal.direction)
    _line("Confidence", f"{signal.confidence}%")

    if hasattr(signal, "entry") and signal.entry is not None:
        _line("Entry", signal.entry)

    if hasattr(signal, "stop_loss") and signal.stop_loss is not None:
        _line("Stop Loss", signal.stop_loss)

    if hasattr(signal, "take_profit") and signal.take_profit is not None:
        _line("Take Profit", signal.take_profit)

    if hasattr(signal, "reason") and signal.reason:
        _line("Reason", signal.reason)

    _footer("Trading Signal")
    
    # ==========================================================
# Candle Report
# ==========================================================

def print_candles(candles):
    """
    Print analyzed candles.
    """

    _section("Candles")

    if not candles:

        _empty("No candles available.")

        _footer("Candles")
        return

    total = len(candles)

    for index, candle in enumerate(candles, start=1):

        print(f"CANDLE {index}/{total}")
        _divider()

        _print_candle(candle)

        if index != total:
            print()

    _footer("Candles")