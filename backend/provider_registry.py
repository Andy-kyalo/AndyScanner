"""
provider_registry.py

Provider Registry.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.providers.base_provider import BaseProvider


class ProviderRegistry:
    """
    Stores all available provider classes.
    """

    def __init__(self):

        self._providers: dict[str, type[BaseProvider]] = {}

    # ==================================================
    # Registration
    # ==================================================

    def register(
        self,
        name: str,
        provider_class: type[BaseProvider],
    ) -> None:
        """
        Register a provider.
        """

        self._providers[name.upper()] = provider_class

    # ==================================================
    # Lookup
    # ==================================================

    def get(
        self,
        name: str,
    ) -> type[BaseProvider] | None:
        """
        Return provider class.
        """

        return self._providers.get(name.upper())

    # ==================================================
    # Information
    # ==================================================

    def names(self) -> list[str]:
        """
        Return registered provider names.
        """

        return sorted(self._providers.keys())

    def exists(self, name: str) -> bool:
        """
        Check whether a provider exists.
        """

        return name.upper() in self._providers

    def count(self) -> int:
        """
        Return number of registered providers.
        """

        return len(self._providers)

    def clear(self) -> None:
        """
        Remove all providers.
        """

        self._providers.clear()