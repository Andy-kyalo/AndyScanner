"""
environment.py

Environment information.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import os
import platform

from config.config import Config


def print_environment():
    """
    Display runtime environment.
    """

    print("\n========== ENVIRONMENT ==========")
    print(f"Operating System : {platform.system()}")
    print(f"OS Version       : {platform.release()}")
    print(f"Architecture     : {platform.machine()}")
    print(f"Working Directory: {os.getcwd()}")
    print(
        f"Database         : "
        f"{os.path.abspath(Config.DATABASE_PATH)}"
    )
    print(
        f"Data Directory   : "
        f"{os.path.abspath(Config.DATA_DIRECTORY)}"
    )
    print("=================================")