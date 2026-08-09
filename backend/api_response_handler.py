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

        if response is None:
            raise APIError(
                code=500,
                message="Response is None.",
            )

        if response.status_code < 200 or response.status_code >= 300:
            raise APIError(
                code=response.status_code,
                message=(
                    f"HTTP {response.status_code}: "
                    f"{response.text}"
                ),
            )

        return response

    # ==================================================
    # Parse JSON
    # ==================================================

    @staticmethod
    def parse(response):
        """
        Validate and parse a JSON response.
        """

        APIResponseHandler.validate(response)

        try:

            return response.json()

        except ValueError as error:

            raise APIError(
                code=500,
                message="Invalid JSON response.",
                details=str(error),
            )