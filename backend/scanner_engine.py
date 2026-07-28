"""
scanner_engine.py

Core Scanner Engine for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import time
from datetime import datetime

from backend.provider_factory import ProviderFactory
from backend.analyzer import Analyzer
from backend.logger import Logger
from backend.market_validator import MarketValidator
from backend.scanner_config import ScannerConfig
from backend.signal_engine import SignalEngine
from database.database_manager import DatabaseManager


class ScannerEngine:
    """
    Executes one complete market scan.

    Responsibilities:
    - Load market data
    - Validate market data
    - Analyze market structure
    - Generate trading signal
    - Save scan results
    - Write logs
    """

    def __init__(self, scanner_config: ScannerConfig):

        self.config = scanner_config
        self.logger = Logger()

    def run(self):
        """
        Execute one complete market scan.
        """

        start_time = time.time()

        market = self.config.market
        timeframe = self.config.timeframe

        try:

            # ==========================================
            # Session Started
            # ==========================================

            self.logger.session_log("===== SESSION STARTED =====")
            self.logger.session_log(
                f"Started At : {datetime.now():%Y-%m-%d %H:%M:%S}"
            )
            self.logger.session_log(f"Market     : {market}")
            self.logger.session_log(f"Timeframe  : {timeframe}")

            self.logger.info(
                "Scanner",
                "Starting market scan."
            )

            # ==========================================
            # Database
            # ==========================================

            with DatabaseManager() as database:

                # ==========================================
                # Load Market Data
                # ==========================================

                provider = ProviderFactory.create(self.config)
                candles = provider.load()

                self.logger.session_log(
                    f"Candles Loaded : {len(candles)}"
                )

                # ==========================================
                # Validate Market Data
                # ==========================================

                validator = MarketValidator(candles)

                if not validator.validate():

                    raise ValueError(
                        "Market data validation failed."
                    )

                self.logger.info(
                    "Validator",
                    "Market data validation passed."
                )

                # ==========================================
                # Analyze Market
                # ==========================================

                analyzer = Analyzer(candles)

                signal_engine = SignalEngine(analyzer)
                signal = signal_engine.generate()

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