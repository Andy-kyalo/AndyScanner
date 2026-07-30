"""
scanner_engine.py

Core Scanner Engine for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import time
from datetime import datetime

from backend.analyzer import Analyzer
from backend.logger import Logger
from backend.market_validator import MarketValidator
from backend.register_providers import register_providers
from backend.scanner_config import ScannerConfig
from backend.signal_engine import SignalEngine
from backend.provider_factory import ProviderFactory
from backend.provider_retry import ProviderRetry
from backend.provider_timeout import ProviderTimeout
from database.database_manager import DatabaseManager


class ScannerEngine:
    """
    Executes one complete market scan.

    Responsibilities
    ----------------
    • Acquire provider
    • Load market data
    • Validate market data
    • Analyze market
    • Generate signal
    • Persist results
    • Log execution
    """

    def __init__(self, scanner_config: ScannerConfig):

        self.config = scanner_config
        self.logger = Logger()

    # ==================================================
    # Execute Scan
    # ==================================================

    def run(self):

        start_timer = time.time()

        scan_time = datetime.now()

        market = self.config.market
        timeframe = self.config.timeframe

        provider_manager = register_providers()

        try:

            # ==================================================
            # Session Started
            # ==================================================

            self.logger.session_log("=" * 60)
            self.logger.session_log("SESSION STARTED")
            self.logger.session_log("=" * 60)

            self.logger.session_log(
                f"Started At : {scan_time:%Y-%m-%d %H:%M:%S}"
            )

            self.logger.session_log(
                f"Market     : {market}"
            )

            self.logger.session_log(
                f"Timeframe  : {timeframe}"
            )

            self.logger.info(
                "Scanner",
                "Starting market scan."
            )

            # ==================================================
            # Provider
            # ==================================================

            factory = ProviderFactory(provider_manager)

            provider = factory.create(self.config)

            provider_manager.record_success()

            self.logger.info(
                "Scanner",
                f"Using provider: {provider.name}"
            )

            self.logger.session_log(
                f"Provider   : {provider.name}"
            )

            # ==================================================
            # Load Market Data
            # ==================================================

            timeout = ProviderTimeout(timeout=10.0)

            retry = ProviderRetry(
                retries=3,
                delay=1.0,
            )

            candles = retry.execute(
                lambda: timeout.execute(provider.load)
            )

            self.logger.session_log(
                f"Candles    : {len(candles)}"
            )

            # ==================================================
            # Validate Market Data
            # ==================================================

            validator = MarketValidator(candles)

            if not validator.validate():

                raise ValueError(
                    "Market data validation failed."
                )

            self.logger.info(
                "Validator",
                "Market data validation passed."
            )

            # ==================================================
            # Analyze Market
            # ==================================================

            analyzer = Analyzer(candles)

            trend = analyzer.trend()

            signal = SignalEngine(
                analyzer
            ).generate()

            signal.market = market
            signal.timeframe = timeframe

            # ==================================================
            # Save Results
            # ==================================================

            with DatabaseManager() as database:

                if not database.scan_exists(
                    market,
                    timeframe,
                    scan_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                ):

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
                        "Scan saved successfully."
                    )

                else:

                    self.logger.info(
                        "Database",
                        "Duplicate scan detected."
                    )

            # ==================================================
            # Logging
            # ==================================================

            duration = round(
                time.time() - start_timer,
                4,
            )

            self.logger.signal_log(
                (
                    f"{market} | "
                    f"{timeframe} | "
                    f"{signal.direction} | "
                    f"{signal.confidence}%"
                )
            )

            self.logger.session_log(
                f"Trend          : {trend}"
            )

            self.logger.session_log(
                f"Signal         : {signal.direction}"
            )

            self.logger.session_log(
                f"Confidence     : {signal.confidence}%"
            )

            self.logger.session_log(
                f"Execution Time : {duration} sec"
            )

            self.logger.session_log(
                "Status         : SUCCESS"
            )

            self.logger.session_log("=" * 60)
            self.logger.session_log("SESSION COMPLETED")
            self.logger.session_log("=" * 60)

            self.logger.info(
                "Scanner",
                "Scan completed successfully."
            )

            return {
                "candles": candles,
                "analyzer": analyzer,
                "signal": signal,
            }

        except Exception as error:

            try:
                provider_manager.record_failure()
            except Exception:
                pass

            self.logger.error_log(
                f"ScannerEngine failed: {error}"
            )

            self.logger.session_log(
                "Status : FAILED"
            )

            self.logger.session_log(
                f"Reason : {error}"
            )

            self.logger.session_log("=" * 60)
            self.logger.session_log("SESSION TERMINATED")
            self.logger.session_log("=" * 60)

            raise