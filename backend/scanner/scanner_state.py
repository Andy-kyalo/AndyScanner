"""
scanner_state.py

Scanner execution state.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from enum import Enum


class ScannerState(Enum):
    """
    Scanner lifecycle states.
    """

    IDLE = "IDLE"

    STARTING = "STARTING"

    RUNNING = "RUNNING"

    PAUSED = "PAUSED"

    STOPPING = "STOPPING"

    STOPPED = "STOPPED"

    ERROR = "ERROR"