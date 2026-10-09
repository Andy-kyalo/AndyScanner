"""
duplicate_candles.py

Detects duplicate candle timestamps.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""

from datetime import datetime, timezone


class DuplicateCandlesValidator:
    """
    Detects duplicate candle timestamps after UTC normalization.
    """

    TIMESTAMP_FORMATS = (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
    )

    @classmethod
    def _parse_timestamp(cls, value):
        """Parse supported timestamps and normalize them to UTC."""

        if isinstance(value, datetime):
            if value.tzinfo is None:
                return value.replace(tzinfo=timezone.utc)
            return value.astimezone(timezone.utc)

        if not isinstance(value, str):
            raise ValueError(
                "Unsupported candle timestamp type: "
                f"{type(value).__name__}"
            )

        value = value.strip()

        # Support ISO-8601 strings, including Z and UTC offsets.
        iso_value = (
            value[:-1] + "+00:00"
            if value.endswith(("Z", "z"))
            else value
        )

        try:
            parsed = datetime.fromisoformat(iso_value)
            if parsed.tzinfo is None:
                return parsed.replace(tzinfo=timezone.utc)
            return parsed.astimezone(timezone.utc)
        except ValueError:
            pass

        # Preserve support for the existing legacy formats.
        for timestamp_format in cls.TIMESTAMP_FORMATS:
            try:
                parsed = datetime.strptime(
                    value,
                    timestamp_format,
                )
                return parsed.replace(tzinfo=timezone.utc)
            except ValueError:
                continue

        raise ValueError(
            f"Unsupported candle timestamp format: {value}"
        )

    def validate(self, candles):
        """Reject duplicate timestamps representing the same instant."""

        timestamps = set()

        for candle in candles:
            try:
                timestamp = self._parse_timestamp(candle.time)
            except (ValueError, TypeError, AttributeError) as error:
                return False, str(error)

            if timestamp in timestamps:
                return (
                    False,
                    f"Duplicate candle detected at {candle.time}.",
                )

            timestamps.add(timestamp)

        return True, "Duplicate candle validation passed."