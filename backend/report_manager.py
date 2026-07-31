"""
report_manager.py

Handles all console reporting.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from config.config import Config
from database.database_manager import DatabaseManager

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


class ReportManager:
    """
    Central reporting service.

    Responsible for displaying scanner reports,
    database reports and future monitoring reports.
    """

    # ==================================================
    # Scanner Report
    # ==================================================

    def print_scan_report(self, candles, analyzer):
        """
        Print the complete scanner report.
        """

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

    # ==================================================
    # Database Report
    # ==================================================

    def print_database_report(self):
        """
        Print every database report.
        """

        with DatabaseManager(Config.DATABASE_PATH) as database:

            self._print_latest_scan(database)

            self._print_scan_history(database)

            self._print_database_statistics(database)

    # ==================================================
    # Latest Scan
    # ==================================================

    def _print_latest_scan(self, database):
        """
        Print the latest scan.
        """

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

        else:

            print("No scans found.")

        print("===============================================")

    # ==================================================
    # Scan History
    # ==================================================

    def _print_scan_history(self, database):
        """
        Print scan history.
        """

        print("\n========== Scan History ==========")

        scans = database.get_all_scans()

        if scans:

            for scan in scans:

                print("----------------------------------")
                print(f"ID          : {scan[0]}")
                print(f"Market      : {scan[1]}")
                print(f"Timeframe   : {scan[2]}")
                print(f"Scan Time   : {scan[3]}")
                print(f"Trend       : {scan[4]}")
                print(f"Signal      : {scan[5]}")
                print(f"Confidence  : {scan[6]}%")

        else:

            print("No scan history available.")

        print("==================================")

    # ==================================================
    # Database Statistics
    # ==================================================

    def _print_database_statistics(self, database):
        """
        Print database statistics.
        """

        print("\n========== Database Statistics ==========")

        statistics = database.get_database_statistics()

        print(f"Total Scans        : {statistics['total_scans']}")
        print(f"Total Signals      : {statistics['total_signals']}")
        print(f"BUY Signals        : {statistics['buy_signals']}")
        print(f"SELL Signals       : {statistics['sell_signals']}")
        print(f"WAIT Signals       : {statistics['wait_signals']}")
        print(
            f"Average Confidence : "
            f"{statistics['average_confidence']}%"
        )

        print("=========================================")

    # ==================================================
    # Future Reports
    # ==================================================

    def print_provider_report(self):
        """
        Reserved for provider reporting.
        """
        pass

    def print_session_report(self):
        """
        Reserved for scanner session reporting.
        """
        pass

    def print_performance_report(self):
        """
        Reserved for performance reporting.
        """
        pass

    def print_signal_statistics(self):
        """
        Reserved for signal statistics.
        """
        pass

    def print_ai_report(self):
        """
        Reserved for AI learning reports.
        """
        pass