"""
health_checker.py

System health checker for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.dependency_checker import DependencyChecker
from backend.validator import Validator


class HealthChecker:
    """
    Performs a complete system health check.
    """

    @staticmethod
    def run() -> dict:
        """
        Run all system health checks.

        Returns
        -------
        dict
            Dictionary containing validation results,
            dependency results and overall health status.
        """

        # ======================================================
        # Configuration Validation
        # ======================================================

        validator_ok, validator_errors = Validator.validate()

        # ======================================================
        # Dependency Validation
        # ======================================================

        dependency_ok, missing_packages = (
            DependencyChecker.check()
        )

        # ======================================================
        # Overall Health
        # ======================================================

        healthy = (
            validator_ok
            and dependency_ok
        )

        return {
            "healthy": healthy,
            "validator_ok": validator_ok,
            "validator_errors": validator_errors,
            "dependency_ok": dependency_ok,
            "missing_packages": missing_packages,
        }