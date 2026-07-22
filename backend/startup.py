"""
startup.py

Application startup utilities for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime
import platform
import sys

from config.config import Config


def print_startup() -> None:
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
    print(f"OS Version  : {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Executable  : {sys.executable}")
    print(
        "Started At  : "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    print("==================================")