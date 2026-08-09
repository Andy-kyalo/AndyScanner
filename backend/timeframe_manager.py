"""
timeframe_manager.py

Central manager for supported Andy Scanner timeframes.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""


class TimeframeManager:
    """
    Manages supported market-data timeframes.
    """

    TIMEFRAME_MAP = {
        "M1": 60,
        "M5": 300,
        "M15": 900,
        "M30": 1800,
        "H1": 3600,
        "H4": 14400,
        "D1": 86400,
    }

    # ==================================================
    # Normalize
    # ==================================================

    @staticmethod
    def normalize(timeframe):
        """
        Normalize a timeframe value.
        """

        if timeframe is None:
            return None

        return str(timeframe).strip().upper()

    # ==================================================
    # Supported Timeframes
    # ==================================================

    @classmethod
    def supported_timeframes(cls):
        """
        Return all supported timeframes.
        """

        return list(cls.TIMEFRAME_MAP.keys())

    # ==================================================
    # Validate
    # ==================================================

    @classmethod
    def is_supported(cls, timeframe):
        """
        Check whether a timeframe is supported.
        """

        timeframe = cls.normalize(timeframe)

        return timeframe in cls.TIMEFRAME_MAP

    # ==================================================
    # Duration
    # ==================================================

    @classmethod
    def seconds(cls, timeframe):
        """
        Return timeframe duration in seconds.

        Raises
        ------
        ValueError
            If the timeframe is unsupported.
        """

        timeframe = cls.normalize(timeframe)

        if not cls.is_supported(timeframe):
            raise ValueError(
                f"Unsupported timeframe '{timeframe}'. "
                f"Supported timeframes: "
                f"{', '.join(cls.supported_timeframes())}"
            )

        return cls.TIMEFRAME_MAP[timeframe]

    # ==================================================
    # Validate Or Raise
    # ==================================================

    @classmethod
    def validate(cls, timeframe):
        """
        Validate and return the normalized timeframe.
        """

        timeframe = cls.normalize(timeframe)

        if not cls.is_supported(timeframe):
            raise ValueError(
                f"Unsupported timeframe '{timeframe}'. "
                f"Supported timeframes: "
                f"{', '.join(cls.supported_timeframes())}"
            )

        return timeframe