"""
main.py

Main entry point for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from config.config import Config

from backend.startup import print_startup
from backend.config_validator import validate_config
from backend.environment import print_environment

from backend.health_checker import HealthChecker

from backend.project_validator import ProjectValidator
from backend.print_validator import print_project_validation

from backend.scanner_engine import ScannerEngine
from backend.scanner_config import ScannerConfig

from backend.report_manager import ReportManager

from backend.register_providers import register_providers

from database.database_manager import DatabaseManager

from backend.scheduler.scheduler_manager import SchedulerManager
from backend.session.scanner_session import ScannerSession

from backend.metrics.performance_metrics import PerformanceMetrics


def main():
    """
    Main Andy Scanner application entry point.
    """

    # ==================================================
    # STARTUP
    # ==================================================

    print_startup()

    validate_config()

    print_environment()

    # ==================================================
    # SYSTEM HEALTH
    # ==================================================

    health = HealthChecker.run()

    print("\n========== SYSTEM HEALTH ==========")

    print(
        f"Status              : "
        f"{'HEALTHY' if health['healthy'] else 'FAILED'}"
    )

    print(
        f"Validator           : "
        f"{health['validator_ok']}"
    )

    print(
        f"Dependencies        : "
        f"{health['dependency_ok']}"
    )

    print("===================================\n")

    if not health["healthy"]:
        print("System health check failed.")
        return

    # ==================================================
    # PROJECT VALIDATION
    # ==================================================

    project = ProjectValidator().validate()

    print_project_validation(project)

    if not project["valid"]:
        print("Project validation failed.")
        return

    # ==================================================
    # DATABASE INITIALIZATION
    # ==================================================

    with DatabaseManager(
        Config.DATABASE_PATH
    ):
        pass

    # ==================================================
    # PROVIDER REGISTRATION
    # ==================================================

    provider_manager = register_providers()

    # ==================================================
    # SCANNER CONFIGURATION
    # ==================================================

    scanner_config = ScannerConfig(
        market=Config.DEFAULT_MARKET,
        timeframe=Config.DEFAULT_TIMEFRAME,
        data_source=Config.DATA_SOURCE,
        api_url=Config.API_URL,
        api_key=Config.API_KEY,
    )

    # ==================================================
    # SCANNER ENGINE
    # ==================================================

    engine = ScannerEngine(
        scanner_config
    )

    # ==================================================
    # SUPPORT SERVICES
    # ==================================================

    scheduler = SchedulerManager()

    performance = PerformanceMetrics()

    session = ScannerSession(
        market=scanner_config.market,
        timeframe=scanner_config.timeframe,
    )

    # ==================================================
    # EXECUTE SCANNER PIPELINE
    # ==================================================

    pipeline_result = engine.execute_pipeline()

    print("\n========== PIPELINE RESULT ==========")

    print(
        f"Success : {pipeline_result.success}"
    )

    print(
        f"Message : {pipeline_result.message}"
    )

    print("=====================================")

    # ==================================================
    # PIPELINE FAILURE
    # ==================================================

    if not pipeline_result.success:

        print()

        if pipeline_result.error is not None:

            print(
                "ERROR TYPE:",
                type(
                    pipeline_result.error
                ).__name__,
            )

            print(
                "ERROR:",
                pipeline_result.error,
            )

        return

    # ==================================================
    # SCAN RESULT
    # ==================================================

    scan_result = pipeline_result.metadata.get(
        "scan_result"
    )

    if scan_result is None:

        print(
            "ERROR: Pipeline completed successfully "
            "but returned no scan result."
        )

        return

    # ==================================================
    # MARKET DATA
    # ==================================================

    candles = scan_result.candles

    analyzer = scan_result.analyzer

    signal = scan_result.signal

    provider = scan_result.provider

    provider_symbol = (
        scan_result.provider_symbol
    )

    # ==================================================
    # SCANNER SESSION
    # ==================================================

    session.update_scan(

        trend=analyzer.trend(),

        signal=signal.direction,

        confidence=signal.confidence,

        candles_processed=len(candles),

        provider=provider,

        execution_time=0.0,

    )

    # ==================================================
    # PERFORMANCE
    # ==================================================

    performance.register_scan(

        execution_time=0.0,

        candles_processed=len(candles),

    )

    # ==================================================
    # LIVE DATA SUMMARY
    # ==================================================

    print("\n========== LIVE MARKET DATA ==========")

    print(
        f"Market             : "
        f"{scan_result.market}"
    )

    print(
        f"Timeframe          : "
        f"{scan_result.timeframe}"
    )

    print(
        f"Provider            : "
        f"{provider}"
    )

    print(
        f"Provider Symbol     : "
        f"{provider_symbol}"
    )

    print(
        f"Candles             : "
        f"{len(candles)}"
    )

    if candles:

        print(
            f"First Candle        : "
            f"{candles[0].time}"
        )

        print(
            f"Latest Candle       : "
            f"{candles[-1].time}"
        )

    print("=======================================")

    # ==================================================
    # ANALYSIS RESULT
    # ==================================================

    print("\n========== MARKET ANALYSIS ==========")

    print(
        f"Trend              : "
        f"{analyzer.trend()}"
    )

    print(
        f"Signal             : "
        f"{signal.direction}"
    )

    print(
        f"Confidence         : "
        f"{signal.confidence}%"
    )

    print("=====================================")

    # ==================================================
    # REPORTS
    # ==================================================

    report = ReportManager()

    report.print_scan_report(
        candles,
        analyzer,
    )

    report.print_database_report()

    # ==================================================
    # SCHEDULER SUMMARY
    # ==================================================

    print("\n========== SCHEDULER ==========")

    scheduler_summary = (
        scheduler.summary()
    )

    print(
        f"Status         : "
        f"{'RUNNING' if scheduler_summary['running'] else 'STOPPED'}"
    )

    print(
        f"Interval       : "
        f"{scheduler_summary['interval']} seconds"
    )

    print(
        f"Scan Counter   : "
        f"{scheduler_summary['scan_counter']}"
    )

    print(
        f"Session Start  : "
        f"{scheduler_summary['session_start']}"
    )

    print(
        f"Last Scan      : "
        f"{scheduler_summary['last_scan']}"
    )

    print(
        f"Uptime         : "
        f"{scheduler_summary['uptime']}"
    )

    print("================================")

    # ==================================================
    # SCANNER SESSION
    # ==================================================

    session_summary = session.summary()

    print(
        "\n========== SCANNER SESSION =========="
    )

    print(
        f"Session ID         : "
        f"{session_summary['session_id']}"
    )

    print(
        f"Market             : "
        f"{session_summary['market']}"
    )

    print(
        f"Timeframe          : "
        f"{session_summary['timeframe']}"
    )

    print(
        f"Started At         : "
        f"{session_summary['started_at']}"
    )

    print(
        f"Last Scan          : "
        f"{session_summary['last_scan']}"
    )

    print(
        f"Candles Processed  : "
        f"{session_summary['candles_processed']}"
    )

    print(
        f"Trend              : "
        f"{session_summary['trend']}"
    )

    print(
        f"Signal             : "
        f"{session_summary['signal']}"
    )

    print(
        f"Confidence         : "
        f"{session_summary['confidence']}%"
    )

    print(
        f"Provider           : "
        f"{session_summary['provider']}"
    )

    print(
        f"Execution Time     : "
        f"{session_summary['execution_time']}"
    )

    print(
        f"Analysis Status    : "
        f"{session_summary['analysis_status']}"
    )

    print("=====================================")

    # ==================================================
    # PERFORMANCE METRICS
    # ==================================================

    performance_summary = (
        performance.summary()
    )

    print(
        "\n========== PERFORMANCE METRICS =========="
    )

    print(
        f"Started At         : "
        f"{performance_summary['started_at']}"
    )

    print(
        f"Total Scans        : "
        f"{performance_summary['total_scans']}"
    )

    print(
        f"Total Candles      : "
        f"{performance_summary['total_candles']}"
    )

    print(
        f"Last Execution     : "
        f"{performance_summary['last_execution_time']}"
    )

    print(
        f"Average Execution  : "
        f"{performance_summary['average_execution_time']}"
    )

    print(
        f"Scans Per Hour     : "
        f"{performance_summary['scans_per_hour']}"
    )

    print("==========================================")

    # ==================================================
    # PROVIDER METRICS
    # ==================================================

    metrics = (
        provider_manager.metrics_report()
    )

    print(
        "\n========== PROVIDER METRICS =========="
    )

    print(
        f"Requests     : "
        f"{metrics['total_requests']}"
    )

    print(
        f"Successful   : "
        f"{metrics['successful_requests']}"
    )

    print(
        f"Failed       : "
        f"{metrics['failed_requests']}"
    )

    print(
        f"Success Rate : "
        f"{metrics['success_rate']}%"
    )

    print("======================================")

    # ==================================================
    # COMPLETE
    # ==================================================

    print(
        "\nAndy Scanner execution completed."
    )


if __name__ == "__main__":
    main()