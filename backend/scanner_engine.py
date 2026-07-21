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
    Core engine responsible for loading market data,
    analysing it, generating signals and saving results.
    """

    def __init__(self, csv_file):
        """
        Initialize Scanner Engine.
        """

        self.csv_file = csv_file
        self.logger = Logger()

    def run(self):
        """
        Execute one complete market scan.
        """

        start_time = time.time()

        try:

            self.logger.session_log("===== SESSION STARTED =====")
            self.logger.info("Scanner", "Starting market scan.")

            with DatabaseManager(Config.DATABASE_PATH) as database:

                # -----------------------------
                # Load Market Data
                # -----------------------------
                loader = Loader(self.csv_file)
                candles = loader.load()

                self.logger.session_log(
                    f"Market: {Config.DEFAULT_MARKET}"
                )

                self.logger.session_log(
                    f"Timeframe: {Config.DEFAULT_TIMEFRAME}"
                )

                self.logger.session_log(
                    f"Candles Loaded: {len(candles)}"
                )

                # -----------------------------
                # Analyze Market
                # -----------------------------
                analyzer = Analyzer(candles)
                signal = analyzer.generate_signal()

                # Apply configuration values
                signal.market = Config.DEFAULT_MARKET
                signal.timeframe = Config.DEFAULT_TIMEFRAME
                
                
                # -----------------------------
                # Save Results
                # -----------------------------
                scan_time = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                if database.scan_exists(
                    Config.DEFAULT_MARKET,
                    Config.DEFAULT_TIMEFRAME,
                    scan_time,
                ):

                    self.logger.info(
                        "Database",
                        "Duplicate scan detected. Skipping database save.",
                    )

                else:

                    database.save_signal(signal)

                    database.save_scan(
                        market=Config.DEFAULT_MARKET,
                        timeframe=Config.DEFAULT_TIMEFRAME,
                        trend=analyzer.trend(),
                        signal=signal.direction,
                        confidence=signal.confidence,
                    )


                    self.logger.info(
                        "Database",
                        "Scan and signal saved successfully.",
                    )

                # -----------------------------
                # Logs
                # -----------------------------
                self.logger.session_log(
                    f"Signal Direction: {signal.direction}"
                )

                self.logger.session_log(
                    f"Signal Confidence: {signal.confidence}%"
                )

                self.logger.signal_log(
                    f"Market={signal.market} | "
                    f"Timeframe={signal.timeframe} | "
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
                    f"Loaded {len(candles)} candles.",
                )

                self.logger.session_log(
                    f"Scan Duration: {duration} seconds"
                )

                self.logger.session_log("Status: SUCCESS")
                self.logger.session_log(
                    "===== SESSION COMPLETED ====="
                )

                return {
                    "candles": candles,
                    "analyzer": analyzer,
                    "signal": signal,
                }

        except Exception as error:

            self.logger.error_log(
                f"ScannerEngine failed: {error}"
            )

            self.logger.session_log("Status: FAILED")
            self.logger.session_log(
                "===== SESSION TERMINATED ====="
            )

            raise