"""
provider_exceptions.py

Custom exceptions for Andy Scanner market data providers.

Author: Andrew Kyalo
Project: Andy Scanner
"""


class ProviderError(Exception):
    """
    Base exception for all provider-related errors.
    """

    def __init__(self, message: str):
        super().__init__(message)


class ProviderRegistrationError(ProviderError):
    """
    Raised when provider registration fails.
    """

    pass


class ProviderNotFoundError(ProviderError):
    """
    Raised when a requested provider
    has not been registered.
    """

    pass


class ProviderConnectionError(ProviderError):
    """
    Raised when a provider
    cannot establish a connection.
    """

    pass


class ProviderAuthenticationError(ProviderError):
    """
    Raised when authentication fails.
    """

    pass


class ProviderTimeoutError(ProviderError):
    """
    Raised when a provider request
    exceeds the configured timeout.
    """

    pass


class ProviderDataError(ProviderError):
    """
    Raised when invalid or empty
    market data is returned.
    """

    pass


class ProviderUnavailableError(ProviderError):
    """
    Raised when a provider
    is temporarily unavailable.
    """

    pass


class ProviderLoadError(ProviderError):
    """
    Raised when market data
    cannot be loaded.
    """

    pass


class ProviderConfigurationError(ProviderError):
    """
    Raised when provider configuration
    is invalid.
    """

    pass