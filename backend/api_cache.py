"""
api_cache.py

Simple in-memory cache for API responses.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import time


class APICache:
    """
    Simple TTL cache.
    """

    def __init__(self, ttl=60):
        self.ttl = ttl
        self._cache = {}

    # ==================================================
    # Store
    # ==================================================

    def put(self, key, value):
        self._cache[key] = {
            "value": value,
            "time": time.time(),
        }

    # ==================================================
    # Retrieve
    # ==================================================

    def get(self, key):

        item = self._cache.get(key)

        if item is None:
            return None

        if time.time() - item["time"] > self.ttl:
            del self._cache[key]
            return None

        return item["value"]

    # ==================================================
    # Clear
    # ==================================================

    def clear(self):
        self._cache.clear()

    # ==================================================
    # Statistics
    # ==================================================

    def size(self):
        return len(self._cache)