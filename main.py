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
    Andy Scanner Entry Point.
    """

    # ==================================================
    # STARTUP
    # ==================================================

    print_startup()

    validate_config()

    print_environment()

    # ==================================================
    # HEALTH CHECK
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
        return

    # ==================================================
    # PROJECT VALIDATION
    # ==================================================

    project = ProjectValidator().validate()

    print_project_validation(project)

    if not project["valid"]:
        return

    # ==================================================
    # DATABASE INITIALIZATION
    # ==================================================

    with DatabaseManager(Config.DATABASE_PATH):
        pass

    # ==================================================
    # REGISTER PROVIDERS
    # ==================================================

    provider_manager = register_providers()

    # ==================================================
    # SCANNER CONFIGURATION
    # ==================================================

    scanner_config = ScannerConfig(
        market=Config.DEFAULT_MARKET,
        timeframe=Config.DEFAULT_TIMEFRAME,
    )

    # ==================================================
    # CREATE ENGINE
    # ==================================================

    engine = ScannerEngine(scanner_config)

    scheduler = SchedulerManager()
    performance = PerformanceMetrics()

    session = ScannerSession(
        market=scanner_config.market,
        timeframe=scanner_config.timeframe,
    )

    # ==================================================
    # EXECUTE PIPELINE
    # ==================================================

    pipeline_result = engine.execute_pipeline()

    print("\n========== PIPELINE TEST ==========")

    print(f"Success : {pipeline_result.success}")

    print(f"Message : {pipeline_result.message}")

    print("===================================")

    if not pipeline_result.success:
        return

    # ==================================================
    # PIPELINE CONTEXT
    # ==================================================

    scan_result = pipeline_result.metadata["scan_result"]

    candles = scan_result.candles
    analyzer = scan_result.analyzer

    # ==================================================
    # UPDATE SCANNER SESSION
    # ==================================================

    session.update_scan(
        trend=analyzer.trend(),
        signal=scan_result.signal.direction,
        confidence=scan_result.signal.confidence,
        candles_processed=len(candles),
        provider="CSVProvider",
        execution_time=0.0,
      )
      
    performance.register_scan(
        execution_time=0.0,
        candles_processed=len(candles),
    )

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

    print()
    print("========== Scheduler ==========")

    scheduler_summary = scheduler.summary()

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

    print("\n========== Scanner Session ==========")

    print(f"Session ID         : {session_summary['session_id']}")
    print(f"Market             : {session_summary['market']}")
    print(f"Timeframe          : {session_summary['timeframe']}")
    print(f"Started At         : {session_summary['started_at']}")
    print(f"Last Scan          : {session_summary['last_scan']}")
    print(f"Candles Processed  : {session_summary['candles_processed']}")
    print(f"Trend              : {session_summary['trend']}")
    print(f"Signal             : {session_summary['signal']}")
    print(f"Confidence         : {session_summary['confidence']}%")
    print(f"Provider           : {session_summary['provider']}")
    print(f"Execution Time     : {session_summary['execution_time']}")
    print(f"Analysis Status    : {session_summary['analysis_status']}")

    print("=====================================")
    
    
    # ==================================================
    # PERFORMANCE METRICS
    # ==================================================

    performance_summary = performance.summary()

    print("\n========== Performance Metrics ==========")

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

    print("=========================================")

    # ==================================================
    # PROVIDER METRICS
    # ==================================================

    metrics = provider_manager.metrics_report()

    print("\n========== Provider Metrics ==========")

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


if __name__ == "__main__":
    main()