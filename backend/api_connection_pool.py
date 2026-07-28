"""
api_connection_pool.py

Connection Pool for API providers.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from requests import Session


class APIConnectionPool:
    """
    Manages reusable HTTP sessions.
    """

    def __init__(self, size=3):
        self._pool = [
            Session()
            for _ in range(size)
        ]

    # ==================================================
    # Acquire
    # ==================================================

    def acquire(self):
        """
        Get an available session.
        """

        if self._pool:
            return self._pool.pop()

        return Session()

    # ==================================================
    # Release
    # ==================================================

    def release(self, session):
        """
        Return a session to the pool.
        """

        self._pool.append(session)

    # ==================================================
    # Close
    # ==================================================

    def close(self):
        """
        Close every session.
        """

        while self._pool:
            session = self._pool.pop()
            session.close()

    # ==================================================
    # Pool Size
    # ==================================================

    def size(self):
        return len(self._pool)