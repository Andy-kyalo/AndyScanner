"""
configuration_cache.py

Configuration cache.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from copy import deepcopy


class ConfigurationCache:
    """
    Runtime configuration cache.
    """

    def __init__(self):

        self._cache = {}

    # ==========================================
    # Cache
    # ==========================================

    def set(self, key, value):

        self._cache[key] = deepcopy(value)

    # ==========================================
    # Retrieve
    # ==========================================

    def get(self, key, default=None):

        if key not in self._cache:
            return default

        return deepcopy(self._cache[key])

    # ==========================================
    # Exists
    # ==========================================

    def exists(self, key):

        return key in self._cache

    # ==========================================
    # Remove
    # ==========================================

    def remove(self, key):

        self._cache.pop(key, None)

    # ==========================================
    # Clear
    # ==========================================

    def clear(self):

        self._cache.clear()

    # ==========================================
    # Statistics
    # ==========================================

    def size(self):

        return len(self._cache)

    def keys(self):

        return list(self._cache.keys())