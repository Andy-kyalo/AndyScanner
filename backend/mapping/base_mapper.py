"""
base_mapper.py

Base mapper interface for all market data providers.

Every provider-specific mapper must inherit from this class
and implement the map() method.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from abc import ABC, abstractmethod


class BaseMapper(ABC):
    """
    Base class for every market data mapper.
    """

    def __init__(self):
        self.source = None

    @abstractmethod
    def map(self, raw_data):
        """
        Convert provider-specific raw data into
        Andy Scanner Candle objects.

        Parameters
        ----------
        raw_data : Any
            Raw provider data.

        Returns
        -------
        list
            List of Candle objects.
        """
        raise NotImplementedError

    def validate(self, raw_data):
        """
        Basic validation before mapping.
        """

        if raw_data is None:
            raise ValueError(
                "Raw data cannot be None."
            )

        if len(raw_data) == 0:
            raise ValueError(
                "Raw data is empty."
            )

        return True

    @property
    def provider(self):
        """
        Provider name.
        """

        return self.__class__.__name__

    def info(self):
        """
        Mapper information.
        """

        return {
            "provider": self.provider,
            "source": self.source,
        }