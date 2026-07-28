"""
api_response_handler.py

API Response Handler.

Validates and parses API responses.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.api_error import APIError


class APIResponseHandler:
    """
    Handles API responses.
    """

    # ==================================================
    # Validate
    # ==================================================

    @staticmethod
    def validate(response):
        """
        Validate an HTTP response.
        """

        if response.status_code != 200:
            raise APIError(
                f"HTTP {response.status_code}: "
                f"{response.text}"
            )

        return response

    # ==================================================
    # Parse JSON
    # ==================================================

    @staticmethod
    def parse(response):
        """
        Parse JSON response.
        """

        APIResponseHandler.validate(response)

        return response.json()