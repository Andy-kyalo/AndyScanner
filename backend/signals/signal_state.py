"""
signal_state.py

Signal lifecycle states.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from enum import Enum


class SignalState(Enum):
    """
    Signal processing states.
    """

    CREATED = "CREATED"

    QUEUED = "QUEUED"

    PROCESSING = "PROCESSING"

    DISPATCHED = "DISPATCHED"

    FAILED = "FAILED"

    EXPIRED = "EXPIRED"

    CANCELLED = "CANCELLED"