"""
api_provider.py

API Market Data Provider.

Concrete provider built on the shared REST API infrastructure.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.api_provider import APIProvider as RESTAPIProvider


class APIProvider(RESTAPIProvider):
    """
    Concrete REST API market-data provider.

    Uses the shared API infrastructure for:

    - API sessions
    - response caching
    - retry handling
    - rate limiting
    - connection pooling
    - request building
    - response parsing
    """

    def __init__(self, config):
        super().__init__(config)

    # ==================================================
    # Load Market Data
    # ==================================================

    def load(self):
        """
        Load market data from the configured API.

        The concrete endpoint will be connected in
        the next stage.
        """

        raise NotImplementedError(
            "Concrete API endpoint has not been configured yet."
        )
