"""
dependency_checker.py

Checks whether all required Python packages
are installed for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import importlib


class DependencyChecker:
    """
    Verifies that all required Python packages
    are installed.
    """

    # ==========================================================
    # Required Packages
    # ==========================================================

    REQUIRED_PACKAGES = {
        "flask": "flask",
        "requests": "requests",
        "dotenv": "python-dotenv",
    }

    # ==========================================================
    # Dependency Check
    # ==========================================================

    @classmethod
    def check(cls):
        """
        Check whether all required packages
        are installed.

        Returns
        -------
        tuple(bool, list)
            (status, missing_packages)
        """

        missing_packages = []

        for module, package in cls.REQUIRED_PACKAGES.items():

            try:
                importlib.import_module(module)

            except ImportError:
                missing_packages.append(package)

        return (
            len(missing_packages) == 0,
            missing_packages,
        )