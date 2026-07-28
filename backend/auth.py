"""
auth.py

Authentication Manager for Andy Scanner.

Provides authentication headers for API providers.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from typing import Dict


class AuthManager:
    """
    Handles API authentication.
    """

    def __init__(
        self,
        api_key: str = "",
        bearer_token: str = "",
    ):

        self.api_key = api_key
        self.bearer_token = bearer_token

    # ==========================================
    # API Key Header
    # ==========================================

    def api_key_header(self) -> Dict[str, str]:

        if not self.api_key:
            return {}

        return {
            "X-API-Key": self.api_key
        }

    # ==========================================
    # Bearer Token Header
    # ==========================================

    def bearer_header(self) -> Dict[str, str]:

        if not self.bearer_token:
            return {}

        return {
            "Authorization": (
                f"Bearer {self.bearer_token}"
            )
        }

    # ==========================================
    # Combined Headers
    # ==========================================

    def headers(self) -> Dict[str, str]:

        headers = {}

        headers.update(self.api_key_header())
        headers.update(self.bearer_header())

        return headers

    # ==========================================
    # Update Credentials
    # ==========================================

    def set_api_key(self, api_key: str):

        self.api_key = api_key

    def set_bearer_token(self, token: str):

        self.bearer_token = token

    # ==========================================
    # Clear Credentials
    # ==========================================

    def clear(self):

        self.api_key = ""
        self.bearer_token = ""