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

from backend.validation.validators.freshness_validator import (
    FreshnessValidator,
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

        ]

        self.timeframe_validator = TimeframeValidator()

        self.freshness_validator = FreshnessValidator()

    # ==================================================
    # Validation
    # ==================================================

    def validate(
        self,
        candles,
        timeframe,
    ):
        """
        Execute the complete market validation pipeline.

        Validation order:

            1. Empty response
            2. Minimum candle availability
            3. Duplicate candles
            4. Invalid prices
            5. Timeframe consistency
            6. Data freshness

        Returns
        -------
        tuple(bool, str)
            Validation result and explanatory message.
        """

        # --------------------------------------------------
        # Standard market-data validators
        # --------------------------------------------------

        for validator in self.validators:

            valid, message = validator.validate(
                candles,
            )

            if not valid:

                return (
                    False,
                    message,
                )

        # --------------------------------------------------
        # Timeframe validation
        # --------------------------------------------------

        valid, message = self.timeframe_validator.validate(
            candles,
            timeframe,
        )

        if not valid:

            return (
                False,
                message,
            )

        # --------------------------------------------------
        # Freshness validation
        # --------------------------------------------------

        valid, message = self.freshness_validator.validate(
            candles,
            timeframe,
        )

        if not valid:

            return (
                False,
                message,
            )

        # --------------------------------------------------
        # Validation successful
        # --------------------------------------------------

        return (
            True,
            "Market data validation passed.",
        )