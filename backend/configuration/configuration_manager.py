"""
configuration_manager.py

Central configuration manager.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from copy import deepcopy

from backend.configuration.configuration_cache import (
    ConfigurationCache,
)
from backend.configuration.configuration_loader import (
    ConfigurationLoader,
)


class ConfigurationManager:
    """
    Central configuration manager.

    Responsibilities
    ----------------
    • Load configuration
    • Cache configuration
    • Retrieve values
    • Update values
    • Reload configuration
    """

    def __init__(
        self,
        profile="production",
        overrides=None,
    ):

        self._loader = ConfigurationLoader()
        self._cache = ConfigurationCache()

        self.load(profile, overrides)

    # ==================================================
    # Load Configuration
    # ==================================================

    def load(
        self,
        profile="production",
        overrides=None,
    ):

        configuration = self._loader.load(
            profile=profile,
            overrides=overrides,
        )

        self._cache.set(
            "configuration",
            configuration,
        )

    # ==================================================
    # Get Configuration
    # ==================================================

    def configuration(self):

        return deepcopy(
            self._cache.get("configuration")
        )

    # ==================================================
    # Get Value
    # ==================================================

    def get(
        self,
        key,
        default=None,
    ):

        configuration = self.configuration()

        return configuration.get(
            key,
            default,
        )

    # ==================================================
    # Set Value
    # ==================================================

    def set(
        self,
        key,
        value,
    ):

        configuration = self.configuration()

        configuration[key] = value

        self._cache.set(
            "configuration",
            configuration,
        )

    # ==================================================
    # Reload
    # ==================================================

    def reload(
        self,
        profile="production",
        overrides=None,
    ):

        self.load(
            profile=profile,
            overrides=overrides,
        )