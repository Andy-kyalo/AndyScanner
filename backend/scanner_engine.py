"""
scanner_engine.py

Core Scanner Engine for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import time
from datetime import datetime

from backend.loader import Loader
from backend.analyzer import Analyzer
from backend.logger import Logger

from database.database_manager import DatabaseManager
from config.config import Config


class ScannerEngine:
    """
    Executes one complete market scan.

    Responsibilities:
    - Load market data
    - Analyze market structure
    - Generate trading signal
    - Save scan results
    - Write logs
    """

    def __init__(self, csv_file):
        """
        Initialize the Scanner Engine.
        """
        self.csv_file = csv_file
        self.logger = Logger()

    def run(self):
        """
        Execute a complete market scan.
        """

        start_time = time.time()

        market = Config.DEFAULT_MARKET
        timeframe = Config.DEFAULT_TIMEFRAME

        try:

            # ==========================================
            # Session Started
            # ==========================================

            self.logger.session_log("===== SESSION STARTED =====")
            self.logger.session_log(
                f"Started At : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            self.logger.session_log(f"Market     : {market}")
            self.logger.session_log(f"Timeframe  : {timeframe}")

            self.logger.info(
                "Scanner",
                "Starting market scan."
            )

            with DatabaseManager(Config.DATABASE_PATH) as database:

                # ==========================================
                # Load Market Data
                # ==========================================

                loader = Loader(self.csv_file)
                candles = loader.load()

                self.logger.session_log(
                    f"Candles Loaded : {len(candles)}"
                )

                # ==========================================
                # Analyze Market
                # ==========================================

                analyzer = Analyzer(candles)
                signal = analyzer.generate_signal()

                signal.market = market
                signal.timeframe = timeframe

                trend = analyzer.trend()

                # ==========================================
                # Save Results
                # ==========================================

                scan_time = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                if database.scan_exists(
                    market,
                    timeframe,
                    scan_time,
                ):

                    self.logger.info(
                        "Database",
                        "Duplicate scan detected. Skipping save."
                    )

                else:

                    database.save_signal(signal)

                    database.save_scan(
                        market=market,
                        timeframe=timeframe,
                        trend=trend,
                        signal=signal.direction,
                        confidence=signal.confidence,
                    )

                    self.logger.info(
                        "Database",
                        "Scan and signal saved successfully."
                    )

                # ==========================================
                # Logging
                # ==========================================

                self.logger.session_log(
                    f"Trend              : {trend}"
                )

                self.logger.session_log(
                    f"Signal Direction   : {signal.direction}"
                )

                self.logger.session_log(
                    f"Signal Confidence  : {signal.confidence}%"
                )

                self.logger.signal_log(
                    f"Market={market} | "
                    f"Timeframe={timeframe} | "
                    f"Direction={signal.direction} | "
                    f"Confidence={signal.confidence}%"
                )

                duration = round(
                    time.time() - start_time,
                    4,
                )

                self.logger.info(
                    "Scanner",
                    f"Scan completed successfully. "
                    f"Loaded {len(candles)} candles."
                )

                self.logger.session_log(
                    f"Scan Duration : {duration} seconds"
                )

                self.logger.session_log("Status : SUCCESS")
                self.logger.session_log(
                    "===== SESSION COMPLETED ====="
                )

                # ==========================================
                # Return Results
                # ==========================================

                return {
                    "candles": candles,
                    "analyzer": analyzer,
                    "signal": signal,
                }

        except Exception as error:

            self.logger.error_log(
                f"ScannerEngine failed: {error}"
            )

            self.logger.session_log("Status : FAILED")
            self.logger.session_log(
                "===== SESSION TERMINATED ====="
            )

            raise