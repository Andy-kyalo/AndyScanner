"""
api_response.py

Standard API Response Model.

Provides a consistent response structure for every
API request made by Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime
from typing import Any


class APIResponse:
    """
    Standard API response object.
    """

    def __init__(
        self,
        success: bool,
        message: str,
        data: Any = None,
    ):

        self.success = success
        self.message = message
        self.data = data

        self.timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    # ==========================================
    # Dictionary Representation
    # ==========================================

    def to_dict(self):

        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "timestamp": self.timestamp,
        }

    # ==========================================
    # String Representation
    # ==========================================

    def __repr__(self):

        return (
            f"APIResponse("
            f"success={self.success}, "
            f"message='{self.message}')"
        )