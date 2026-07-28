"""
http_client.py

HTTP Client for Andy Scanner.

Provides standard GET and POST requests with
timeout handling and error management.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import requests

from backend.api_response import APIResponse
from backend.api_error import APIError


class HTTPClient:
    """
    Standard HTTP client.
    """

    def __init__(self, timeout=10):

        self.timeout = timeout

    # ==========================================
    # GET Request
    # ==========================================

    def get(self, url, headers=None, params=None):

        try:

            response = requests.get(
                url=url,
                headers=headers,
                params=params,
                timeout=self.timeout,
            )

            response.raise_for_status()

            return APIResponse(
                success=True,
                message="GET request successful.",
                data=response.json(),
            )

        except requests.exceptions.RequestException as error:

            raise APIError(
                code=500,
                message="GET request failed.",
                details=str(error),
            )

    # ==========================================
    # POST Request
    # ==========================================

    def post(
        self,
        url,
        headers=None,
        json=None,
    ):

        try:

            response = requests.post(
                url=url,
                headers=headers,
                json=json,
                timeout=self.timeout,
            )

            response.raise_for_status()

            return APIResponse(
                success=True,
                message="POST request successful.",
                data=response.json(),
            )

        except requests.exceptions.RequestException as error:

            raise APIError(
                code=500,
                message="POST request failed.",
                details=str(error),
            )