"""
provider_service.py

Shared ProviderManager instance.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.provider_manager import ProviderManager

_provider_manager = ProviderManager()


def get_provider_manager():
    """
    Return the shared ProviderManager instance.
    """
    return _provider_manager