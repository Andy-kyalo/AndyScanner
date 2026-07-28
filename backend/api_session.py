"""
api_session.py

API Session Manager.

Manages authenticated API sessions for
market data providers.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from requests import Session


class APISession:
    """
    HTTP session manager.
    """

    def __init__(self):
        self._session = Session()

    # ==================================================
    # Session
    # ==================================================

    @property
    def session(self):
        return self._session

    # ==================================================
    # Headers
    # ==================================================

    def set_headers(self, headers: dict):
        self._session.headers.update(headers)

    # ==================================================
    # Authentication
    # ==================================================

    def set_token(self, token: str):
        self._session.headers.update(
            {
                "Authorization": f"Bearer {token}"
            }
        )

    # ==================================================
    # Close
    # ==================================================

    def close(self):
        self._session.close()