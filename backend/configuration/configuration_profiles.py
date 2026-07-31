"""
configuration_profiles.py

Configuration profiles.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from copy import deepcopy

from backend.configuration.configuration_defaults import (
    DEFAULT_CONFIGURATION,
)


class ConfigurationProfiles:
    """
    Available configuration profiles.
    """

    def __init__(self):

        self._profiles = {

            "development": {
                "debug": True,
                "log_level": "DEBUG",
            },

            "testing": {
                "debug": True,
                "log_level": "DEBUG",
                "cache_enabled": False,
            },

            "production": {
                "debug": False,
                "log_level": "INFO",
            },
        }

    # ==========================================
    # Load Profile
    # ==========================================

    def load(self, profile):

        profile = profile.lower()

        if profile not in self._profiles:

            raise ValueError(
                f"Unknown configuration profile: {profile}"
            )

        configuration = deepcopy(DEFAULT_CONFIGURATION)

        configuration.update(self._profiles[profile])

        return configuration

    # ==========================================
    # Information
    # ==========================================

    def exists(self, profile):

        return profile.lower() in self._profiles

    def names(self):

        return sorted(self._profiles.keys())