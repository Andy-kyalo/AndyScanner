"""
printer.py

Displays all Andy Scanner analysis results.

Author: Andrew Kyalo
Project: Andy Scanner
"""

# ==========================================
# Analysis
# ==========================================

def print_analysis(analyzer):

    print(f"Total Candles: {len(analyzer.candles)}")
    print()

    print("========== Analysis ==========")
    print(f"Highest High : {analyzer.highest_high()}")
    print(f"Lowest Low   : {analyzer.lowest_low()}")
    print("==============================")
    print()

    print(f"Trend: {analyzer.trend()}")
    print()


# ==========================================
# Strongest Candle
# ==========================================

def print_strongest_candle(analyzer):

    strongest = analyzer.strongest_candle()

    print("========== Strongest Candle ==========")
    print(f"Time      : {strongest.time}")
    print(f"Body Size : {strongest.body_size()}")
    print("======================================")
    print()


# ==========================================
# Swing Highs
# ==========================================

def print_swing_highs(analyzer):

    print("========== Swing Highs ==========")

    highs = analyzer.swing_highs()

    if highs:
        for candle in highs:
            print(f"Swing High at {candle.time} | High = {candle.high}")
    else:
        print("No Swing High found.")

    print("=================================")
    print()


# ==========================================
# Swing Lows
# ==========================================

def print_swing_lows(analyzer):

    print("========== Swing Lows ==========")

    lows = analyzer.swing_lows()

    if lows:
        for candle in lows:
            print(f"Swing Low at {candle.time} | Low = {candle.low}")
    else:
        print("No Swing Low found.")

    print("================================")
    print()


# ==========================================
# Break of Structure
# ==========================================

def print_bos(analyzer):

    print("========== Break of Structure ==========")

    if analyzer.bullish_bos():
        print("Bullish BOS detected.")
    else:
        print("No Bullish BOS.")

    print("========================================")
    print()

    print("========== Bearish BOS ==========")

    if analyzer.bearish_bos():
        print("Bearish BOS detected.")
    else:
        print("No Bearish BOS.")

    print("=================================")
    print()


# ==========================================
# Market Structure
# ==========================================

def print_market_structure(analyzer):

    print("========== Market Structure ==========")

    print(f"Trend          : {analyzer.trend()}")
    print(f"Highest High   : {analyzer.highest_high()}")
    print(f"Lowest Low     : {analyzer.lowest_low()}")

    if analyzer.bullish_bos():
        structure = "Bullish Break of Structure"
    elif analyzer.bearish_bos():
        structure = "Bearish Break of Structure"
    else:
        structure = "No Break of Structure"

    print(f"Structure      : {structure}")

    print("======================================")
    print()


# ==========================================
# Engulfing Patterns
# ==========================================

def print_engulfing(analyzer):

    print("========== Engulfing Patterns ==========")

    bullish = analyzer.bullish_engulfing()
    bearish = analyzer.bearish_engulfing()

    if bullish:
        for candle in bullish:
            print(f"Bullish Engulfing at {candle.time}")

    if bearish:
        for candle in bearish:
            print(f"Bearish Engulfing at {candle.time}")

    if not bullish and not bearish:
        print("No Engulfing Pattern.")

    print("========================================")
    print()


# ==========================================
# Order Blocks
# ==========================================

def print_order_blocks(analyzer):

    order_block = analyzer.bullish_order_block()

    print("========== Bullish Order Block ==========")

    if order_block:
        print(f"Time : {order_block.time}")
        print(f"Open : {order_block.open}")
        print(f"High : {order_block.high}")
        print(f"Low  : {order_block.low}")
        print(f"Close: {order_block.close}")
    else:
        print("No Bullish Order Block.")

    print("=========================================")
    print()


# ==========================================
# Change of Character
# ==========================================

def print_choch(analyzer):

    print("========== Change of Character ==========")

    if analyzer.bullish_choch():
        print("Bullish Change of Character.")
    elif analyzer.bearish_choch():
        print("Bearish Change of Character.")
    else:
        print("No Change of Character.")

    print("=========================================")
    print()


# ==========================================
# Fair Value Gap
# ==========================================

def print_fvg(analyzer):

    print("========== Bullish FVG ==========")

    fvgs = analyzer.bullish_fvg()

    if fvgs:
        for first, third in fvgs:
            print(
                f"Gap between {first.time} ({first.high}) "
                f"and {third.time} ({third.low})"
            )
    else:
        print("No Bullish Fair Value Gap.")

    print("=================================")
    print()


# ==========================================
# Liquidity
# ==========================================

def print_liquidity(analyzer):

    print("========== Liquidity ==========")
    print()

    print("Buy-side Liquidity")

    buy = analyzer.buy_side_liquidity()

    if buy:
        for candle in buy:
            print(f"{candle.time} | High = {candle.high}")
    else:
        print("None")

    print()

    print("Sell-side Liquidity")

    sell = analyzer.sell_side_liquidity()

    if sell:
        for candle in sell:
            print(f"{candle.time} | Low = {candle.low}")
    else:
        print("None")

    print("================================")
    print()


# ==========================================
# Trading Signal
# ==========================================

def print_signal(analyzer):

    print("========== Signal ==========")

    signal = analyzer.generate_signal()
    signal.show()

    print()


# ==========================================
# Candles
# ==========================================

def print_candles(candles):

    print("========== Candles ==========")

    for candle in candles:
        candle.show()
        print()