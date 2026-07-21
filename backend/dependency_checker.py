"""
dependency_checker.py

Checks all required Python packages.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import importlib


class DependencyChecker:
    """
    Verifies that required packages are installed.
    """

    REQUIRED_PACKAGES = {
        "flask": "flask",
        "requests": "requests",
        "dotenv": "python-dotenv",
    }

    @classmethod
    def check(cls):
        """
        Returns
        -------
        tuple(bool, list)
        """

        missing = []

        for module, package in cls.REQUIRED_PACKAGES.items():

            try:
                importlib.import_module(module)

            except ImportError:
                missing.append(package)

        return len(missing) == 0, missing