"""
market_validator.py

Professional Market Validation Pipeline.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""

from backend.validation.validators.empty_response import (
    EmptyResponseValidator,
)

from backend.validation.validators.missing_candles import (
    MissingCandlesValidator,
)

from backend.validation.validators.duplicate_candles import (
    DuplicateCandlesValidator,
)

from backend.validation.validators.invalid_prices import (
    InvalidPricesValidator,
)

from backend.validation.validators.timeframe_validator import (
    TimeframeValidator,
)


class MarketValidator:
    """
    Runs the complete market validation pipeline.
    """

    def __init__(self):

        self.validators = [

            EmptyResponseValidator(),

            MissingCandlesValidator(),

            DuplicateCandlesValidator(),

            InvalidPricesValidator(),

            TimeframeValidator(),

        ]

    def validate(self, candles):
        """
        Execute all validators.

        Returns
        -------
        (bool, str)
        """

        for validator in self.validators:

            valid, message = validator.validate(candles)

            if not valid:
                return False, message

        return True, "Market validation passed."