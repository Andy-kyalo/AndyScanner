"""
test_config_validator.py

Configuration validation tests for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import unittest
from unittest.mock import patch

from backend.config_validator import validate_config


class TestConfigValidator(unittest.TestCase):

    def _valid_configuration(self):
        return {
            "APP_NAME": "Andy Scanner",
            "APP_VERSION": "0.5.0",
            "DEFAULT_MARKET": "EURUSD",
            "DEFAULT_TIMEFRAME": "M5",
            "DATABASE_PATH": "database/scanner.db",
            "DATA_SOURCE": "TWELVEDATA",
            "API_KEY": "TEST_API_KEY",
        }

    def test_valid_twelvedata_configuration_passes(self):

        values = self._valid_configuration()

        with patch.multiple(
            "backend.config_validator.Config",
            **values,
        ):

            validate_config()

    def test_missing_twelvedata_api_key_fails(self):

        values = self._valid_configuration()
        values["API_KEY"] = ""

        with patch.multiple(
            "backend.config_validator.Config",
            **values,
        ):

            with self.assertRaises(
                RuntimeError
            ):

                validate_config()

    def test_csv_configuration_does_not_require_api_key(self):

        values = self._valid_configuration()
        values["DATA_SOURCE"] = "CSV"
        values["API_KEY"] = ""

        with patch.multiple(
            "backend.config_validator.Config",
            **values,
        ):

            validate_config()

    def test_missing_core_configuration_fails(self):

        values = self._valid_configuration()
        values["DEFAULT_MARKET"] = ""

        with patch.multiple(
            "backend.config_validator.Config",
            **values,
        ):

            with self.assertRaises(
                RuntimeError
            ):

                validate_config()


if __name__ == "__main__":
    unittest.main()
