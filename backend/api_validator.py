"""
api_validator.py

API Response Validator.

Validates API responses before they are passed
to the scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.api_error import APIError


class APIValidator:
    """
    Validates API responses.
    """

    # ==========================================
    # Validate Response
    # ==========================================

    @staticmethod
    def validate(response):

        if response is None:
            raise APIError(
                code=500,
                message="Response is None."
            )

        return True

    # ==========================================
    # Validate JSON
    # ==========================================

    @staticmethod
    def validate_json(data):

        if not isinstance(data, dict):
            raise APIError(
                code=500,
                message="Invalid JSON response."
            )

        return True

    # ==========================================
    # Validate Candles
    # ==========================================

    @staticmethod
    def validate_candles(candles):

        if candles is None:
            raise APIError(
                code=500,
                message="No candle data received."
            )

        if not isinstance(candles, list):
            raise APIError(
                code=500,
                message="Candles must be a list."
            )

        if len(candles) == 0:
            raise APIError(
                code=500,
                message="Empty candle list."
            )

        return True

    # ==========================================
    # Validate Required Fields
    # ==========================================

    @staticmethod
    def validate_fields(data, required_fields):

        missing = [
            field
            for field in required_fields
            if field not in data
        ]

        if missing:
            raise APIError(
                code=500,
                message="Missing required fields.",
                details=", ".join(missing)
            )

        return True