"""
provider_registry.py

Registry for all market data providers.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.providers.base_provider import BaseProvider
from backend.provider_exceptions import (
    ProviderRegistrationError,
    ProviderNotFoundError,
)


class ProviderRegistry:
    """
    Stores all available provider classes.
    """

    def __init__(self):

        self._providers = {}

    # ==================================================
    # Register
    # ==================================================

    def register(
        self,
        name: str,
        provider_class: type[BaseProvider],
    ) -> None:
        """
        Register a provider.
        """

        key = name.upper()

        if key in self._providers:

            raise ProviderRegistrationError(
                f"Provider '{key}' is already registered."
            )

        self._providers[key] = provider_class

    # ==================================================
    # Get
    # ==================================================

    def get(
        self,
        name: str,
    ) -> type[BaseProvider]:
        """
        Return provider class.
        """

        key = name.upper()

        if key not in self._providers:

            raise ProviderNotFoundError(
                f"Provider '{key}' is not registered."
            )

        return self._providers[key]

    # ==================================================
    # Exists
    # ==================================================

    def exists(
        self,
        name: str,
    ) -> bool:

        return name.upper() in self._providers

    # ==================================================
    # Remove
    # ==================================================

    def unregister(
        self,
        name: str,
    ) -> None:

        key = name.upper()

        if key not in self._providers:

            raise ProviderNotFoundError(
                f"Provider '{key}' is not registered."
            )

        del self._providers[key]

    # ==================================================
    # Clear
    # ==================================================

    def clear(self) -> None:

        self._providers.clear()

    # ==================================================
    # Names
    # ==================================================

    def names(self) -> list[str]:

        return sorted(self._providers.keys())

    # ==================================================
    # Count
    # ==================================================

    def count(self) -> int:

        return len(self._providers)