"""
health_checker.py

System health checker.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.validator import Validator
from backend.dependency_checker import DependencyChecker


class HealthChecker:
    """
    Performs a complete system health check.
    """

    @staticmethod
    def run():
        """
        Returns
        -------
        dict
        """

        validator_ok, validator_errors = Validator.validate()

        dependency_ok, missing_packages = (
            DependencyChecker.check()
        )

        return {
            "validator_ok": validator_ok,
            "validator_errors": validator_errors,
            "dependency_ok": dependency_ok,
            "missing_packages": missing_packages,
            "healthy": (
                validator_ok and dependency_ok
            ),
        }