"""
environment.py

Displays runtime environment information
for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import os
import platform

from config.config import Config


def print_environment() -> None:
    """
    Display runtime environment information.
    """

    print("\n========== ENVIRONMENT ==========")

    print(f"Operating System : {platform.system()}")
    print(f"OS Version       : {platform.release()}")
    print(f"Architecture     : {platform.machine()}")

    print(f"Working Directory: {os.getcwd()}")

    print(
        "Database         : "
        f"{os.path.abspath(Config.DATABASE_PATH)}"
    )

    print(
        "Data Directory   : "
        f"{os.path.abspath(Config.DATA_DIRECTORY)}"
    )

    print(f"Log Level        : {Config.LOG_LEVEL}")
    print(f"Debug Mode       : {Config.DEBUG}")

    print("=================================")