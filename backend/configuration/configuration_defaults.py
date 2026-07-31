"""
configuration_defaults.py

Default configuration values.

Author: Andrew Kyalo
Project: Andy Scanner
"""

DEFAULT_CONFIGURATION = {

    "market": "US30",
    "timeframe": "M5",
    "data_source": "CSV",

    "retry_count": 3,
    "retry_delay": 1.0,

    "provider_timeout": 10.0,

    "debug": False,
    "log_level": "INFO",

    "database_path": "database/scanner.db",

    "cache_enabled": True,
    "cache_ttl": 300,
}