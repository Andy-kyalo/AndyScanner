"""
startup.py

Application startup utilities.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import platform
import sys

from config.config import Config


def print_startup():
    """
    Display application startup information.
    """

    print("\n========== ANDY SCANNER ==========")
    print(f"Application : {Config.APP_NAME}")
    print(f"Version     : {Config.APP_VERSION}")
    print(f"Market      : {Config.DEFAULT_MARKET}")
    print(f"Timeframe   : {Config.DEFAULT_TIMEFRAME}")
    print(f"Python      : {platform.python_version()}")
    print(f"Platform    : {platform.system()}")
    print(f"Executable  : {sys.executable}")
    print("==================================")