"""
configuration_loader.py

Configuration loader.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from copy import deepcopy

from backend.configuration.configuration_defaults import (
    DEFAULT_CONFIGURATION,
)
from backend.configuration.configuration_profiles import (
    ConfigurationProfiles,
)


class ConfigurationLoader:
    """
    Loads Andy Scanner configuration.
    """

    def __init__(self):

        self._profiles = ConfigurationProfiles()

    # ==================================================
    # Default Configuration
    # ==================================================

    def defaults(self):

        return deepcopy(DEFAULT_CONFIGURATION)

    # ==================================================
    # Load Profile
    # ==================================================

    def profile(self, profile_name):

        return self._profiles.load(profile_name)

    # ==================================================
    # Merge
    # ==================================================

    def merge(self, base, override):

        configuration = deepcopy(base)

        configuration.update(override)

        return configuration

    # ==================================================
    # Load
    # ==================================================

    def load(
        self,
        profile="production",
        overrides=None,
    ):

        configuration = self.profile(profile)

        if overrides:

            configuration = self.merge(
                configuration,
                overrides,
            )

        return configuration