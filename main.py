from database.database_manager import DatabaseManager

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

    # ------------------------------------
    # Initialize Database
    # ------------------------------------
    with DatabaseManager():
        pass

    # ------------------------------------
    # Run Scanner
    # ------------------------------------
    engine = ScannerEngine("data/us30.csv")
    result = engine.run()

    candles = result["candles"]
    analyzer = result["analyzer"]

    # ------------------------------------
    # Print Analysis
    # ------------------------------------
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

    # ------------------------------------
    # Database Reports
    # ------------------------------------
    with DatabaseManager() as database:

        print("\n========== Latest Scan From Database ==========")

        latest_scan = database.get_latest_scan()

        if latest_scan:
            print(f"ID          : {latest_scan[0]}")
            print(f"Market      : {latest_scan[1]}")
            print(f"Timeframe   : {latest_scan[2]}")
            print(f"Scan Time   : {latest_scan[3]}")
            print(f"Trend       : {latest_scan[4]}")
            print(f"Signal      : {latest_scan[5]}")
            print(f"Confidence  : {latest_scan[6]}%")

        print("===============================================")

        print("\n========== Scan History ==========")

        all_scans = database.get_all_scans()

        for scan in all_scans:
            print("----------------------------------")
            print(f"ID          : {scan[0]}")
            print(f"Market      : {scan[1]}")
            print(f"Timeframe   : {scan[2]}")
            print(f"Scan Time   : {scan[3]}")
            print(f"Trend       : {scan[4]}")
            print(f"Signal      : {scan[5]}")
            print(f"Confidence  : {scan[6]}%")

        print("==================================")
        print("\n========== Database Statistics ==========")

        statistics = database.get_database_statistics()

        print(f"Total Scans        : {statistics['total_scans']}")
        print(f"Total Signals      : {statistics['total_signals']}")
        print(f"BUY Signals        : {statistics['buy_signals']}")
        print(f"SELL Signals       : {statistics['sell_signals']}")
        print(f"WAIT Signals       : {statistics['wait_signals']}")
        print(f"Average Confidence : {statistics['average_confidence']}%")

        print("=========================================")


if __name__ == "__main__":
    main()