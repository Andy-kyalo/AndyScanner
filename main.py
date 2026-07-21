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

from backend.market_manager import MarketManager
from backend.scanner_engine import ScannerEngine
from backend.report_manager import ReportManager

from database.database_manager import DatabaseManager


def main():
    """
    Run the complete Andy Scanner workflow.
    """

    # ------------------------------------
    # Startup
    # ------------------------------------
    print_startup()
    validate_config()
    print_environment()

    # ------------------------------------
    # System Health Check
    # ------------------------------------
    health = HealthChecker.run()

    print("\n========== SYSTEM HEALTH ==========")

    if health["healthy"]:
        print("Status              : HEALTHY")
    else:
        print("Status              : FAILED")

    print(f"Validator           : {health['validator_ok']}")
    print(f"Dependencies        : {health['dependency_ok']}")

    if health["validator_errors"]:
        print("\nConfiguration Errors:")
        for error in health["validator_errors"]:
            print(f" - {error}")

    if health["missing_packages"]:
        print("\nMissing Packages:")
        for package in health["missing_packages"]:
            print(f" - {package}")

    print("===================================\n")

    if not health["healthy"]:
        return

    # ------------------------------------
    # Project Validation
    # ------------------------------------
    project = ProjectValidator().validate()

    print_project_validation(project)

    if not project["valid"]:
        return

    # ------------------------------------
    # Initialize Database
    # ------------------------------------
    with DatabaseManager(Config.DATABASE_PATH):
        pass

    # ------------------------------------
    # Detect Markets
    # ------------------------------------
    market_manager = MarketManager()

    markets = market_manager.available_markets()

    if not markets:
        raise FileNotFoundError(
            "No market CSV files found in the data directory."
        )

    # ------------------------------------
    # Run Scanner
    # ------------------------------------
    engine = ScannerEngine(str(markets[0]))
    result = engine.run()

    candles = result["candles"]
    analyzer = result["analyzer"]

    # ------------------------------------
    # Reports
    # ------------------------------------
    report = ReportManager()

    report.print_scan_report(candles, analyzer)
    report.print_database_report()


if __name__ == "__main__":
    main()