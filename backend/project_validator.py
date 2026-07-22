"""
project_validator.py

Validates the Andy Scanner project structure.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from pathlib import Path


class ProjectValidator:
    """
    Validates the required project structure.
    """

    # ==========================================================
    # Required Directories
    # ==========================================================

    REQUIRED_DIRECTORIES = [
        "backend",
        "config",
        "database",
        "data",
        "logs",
    ]

    # ==========================================================
    # Required Files
    # ==========================================================

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

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(self):
        """
        Initialize project validator.
        """

        self.base_dir = Path(__file__).resolve().parent.parent

    # ==========================================================
    # Validation
    # ==========================================================

    def validate(self) -> dict:
        """
        Validate the project structure.

        Returns
        -------
        dict
            {
                "valid": bool,
                "missing": list[str]
            }
        """

        missing = []

        # Check required directories
        for directory in self.REQUIRED_DIRECTORIES:

            path = self.base_dir / directory

            if not path.exists() or not path.is_dir():
                missing.append(directory)

        # Check required files
        for file in self.REQUIRED_FILES:

            path = self.base_dir / file

            if not path.exists() or not path.is_file():
                missing.append(file)

        missing.sort()

        return {
            "valid": len(missing) == 0,
            "missing": missing,
        }