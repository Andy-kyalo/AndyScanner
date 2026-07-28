"""
api_error.py

Standard API Error Model.

Provides a consistent error structure for every
API-related operation in Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime


class APIError(Exception):
    """
    Standard API exception.
    """

    def __init__(
        self,
        code: int,
        message: str,
        details: str = "",
    ):

        self.code = code
        self.message = message
        self.details = details

        self.timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        super().__init__(self.message)

    # ==========================================
    # Dictionary Representation
    # ==========================================

    def to_dict(self):

        return {
            "success": False,
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
                "timestamp": self.timestamp,
            },
        }

    # ==========================================
    # String Representation
    # ==========================================

    def __repr__(self):

        return (
            f"APIError("
            f"code={self.code}, "
            f"message='{self.message}')"
        )