"""
project_validator.py

Validates the Andy Scanner project structure.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from pathlib import Path


class ProjectValidator:
    """
    Checks whether the project structure is complete.
    """

    REQUIRED_DIRECTORIES = [
        "backend",
        "config",
        "database",
        "data",
        "logs",
    ]

    REQUIRED_FILES = [
        "main.py",
        "requirements.txt",
        "config/config.py",
        "backend/scanner_engine.py",
        "backend/analyzer.py",
        "backend/loader.py",
        "backend/logger.py",
        "database/database_manager.py",
    ]

    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent

    def validate(self):
        """
        Validate project structure.
        """

        missing = []

        for directory in self.REQUIRED_DIRECTORIES:
            path = self.base_dir / directory

            if not path.exists():
                missing.append(directory)

        for file in self.REQUIRED_FILES:
            path = self.base_dir / file

            if not path.exists():
                missing.append(file)

        return {
            "valid": len(missing) == 0,
            "missing": missing,
        }