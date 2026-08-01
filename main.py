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
    # REPORTS
    # ==================================================

    report = ReportManager()

    report.print_scan_report(
        candles,
        analyzer,
    )

    report.print_database_report()

    # ==================================================
    # SESSION SUMMARY
    # ==================================================

    summary = scan_result.summary()

    print("\n========== Scanner Session ==========")

    print(
        f"Market       : {summary['market']}"
    )

    print(
        f"Timeframe    : {summary['timeframe']}"
    )

    print(
        f"Candles      : {summary['candles']}"
    )

    print(
        f"Trend        : {summary['trend']}"
    )

    print(
        f"Signal       : {summary['signal']}"
    )

    print(
        f"Confidence   : {summary['confidence']}%"
    )

    print("=====================================")

    # ==================================================
    # PROVIDER METRICS
    # ==================================================

    metrics = provider_manager.metrics_report()

    print("\n========== Provider Metrics ==========")

    print(
        f"Requests     : {metrics['total_requests']}"
    )

    print(
        f"Successful   : {metrics['successful_requests']}"
    )

    print(
        f"Failed       : {metrics['failed_requests']}"
    )

    print(
        f"Success Rate : {metrics['success_rate']}%"
    )

    print(
        f"Average Time : {metrics['average_time']} sec"
    )

    print("======================================")


if __name__ == "__main__":
    main()