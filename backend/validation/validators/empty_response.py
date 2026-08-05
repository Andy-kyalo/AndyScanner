"""
empty_response.py

Validates provider responses before processing.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""


class EmptyResponseValidator:
    """
    Validates that a provider returned data.
    """

    def validate(self, response):
        """
        Validate provider response.

        Returns
        -------
        (bool, str)
        """

        if response is None:
            return False, "Provider returned no response."

        if len(response) == 0:
            return False, "Provider returned an empty response."

        return True, "Response validation passed."