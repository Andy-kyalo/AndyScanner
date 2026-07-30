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
from database.database_manager import DatabaseManager
from backend.provider_factory import ProviderFactory
from backend.provider_retry import ProviderRetry
from backend.provider_timeout import ProviderTimeout


class ScannerEngine:
    """
    Executes one complete market scan.

    Responsibilities
    ----------------
    • Load market data
    • Validate provider
    • Validate market data
    • Analyze market
    • Generate trading signal
    • Save scan results
    • Write logs
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

            health = provider_manager.health(provider)

            if not health.check():

                provider_manager.metrics.record_failure()

                raise RuntimeError(
                    f"{provider.name} failed health check."
                )

            provider_manager.metrics.record_success()

            self.logger.session_log(
                f"Provider : {provider.name}"
            )

            # ------------------------------------------
            # Load Market Data
            # ------------------------------------------

            timeout = ProviderTimeout(
                timeout=10.0,
            )

            retry = ProviderRetry(
                retries=3,
                delay=1.0,
            )

            candles = retry.execute(
                lambda: timeout.execute(
                    provider.load
           )
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

            signal_engine = SignalEngine(analyzer)

            signal = signal_engine.generate()

            signal.market = market
            signal.timeframe = timeframe

            # ==================================================
            # Save Results
            # ==================================================

            with DatabaseManager() as database:

                if database.scan_exists(
                    market,
                    timeframe,
                    scan_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                ):

                    self.logger.info(
                        "Database",
                        "Duplicate scan detected."
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
                        "Scan saved successfully."
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

            provider_manager.metrics.record_failure()

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