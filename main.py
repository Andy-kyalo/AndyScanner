from backend.scanner_engine import ScannerEngine
from backend.printer import (
    print_analysis,
    print_strongest_candle,
    print_swing_highs,
    print_swing_lows,
    print_bos,
    print_market_structure,
    print_engulfing,
    print_order_blocks,
    print_choch,
    print_fvg,
    print_liquidity,
    print_signal,
    print_candles,
)


def main():

    engine = ScannerEngine("data/us30.csv")

    result = engine.run()

    candles = result["candles"]
    analyzer = result["analyzer"]

    print_analysis(analyzer)
    print_strongest_candle(analyzer)
    print_swing_highs(analyzer)
    print_swing_lows(analyzer)
    print_bos(analyzer)
    print_market_structure(analyzer)
    print_engulfing(analyzer)
    print_order_blocks(analyzer)
    print_choch(analyzer)
    print_fvg(analyzer)
    print_liquidity(analyzer)
    print_signal(analyzer)
    print_candles(candles)


if __name__ == "__main__":
    main()