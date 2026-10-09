import unittest

from backend.log_redaction import redact_secrets


class TestLogRedaction(unittest.TestCase):

    def test_redacts_api_key_query_parameters(self):
        message = (
            "Request failed: "
            "https://api.example.test/data?symbol=EURUSD"
            "&apikey=SYNTHETIC_SECRET_123&interval=5min"
        )

        result = redact_secrets(message)

        self.assertNotIn("SYNTHETIC_SECRET_123", result)
        self.assertIn("symbol=EURUSD", result)
        self.assertIn("interval=5min", result)
        self.assertIn("REDACTED", result)

    def test_redacts_common_api_key_parameter_names(self):
        for parameter in ("api_key", "API_KEY", "access_token"):
            with self.subTest(parameter=parameter):
                message = f"https://example.test/?{parameter}=SYNTHETIC_SECRET_456"
                result = redact_secrets(message)
                self.assertNotIn("SYNTHETIC_SECRET_456", result)
                self.assertIn("REDACTED", result)

    def test_redacts_bearer_tokens_and_auth_headers(self):
        message = (
            "Authorization: Bearer SYNTHETIC_BEARER_789; "
            "X-API-Key: SYNTHETIC_HEADER_ABC"
        )

        result = redact_secrets(message)

        self.assertNotIn("SYNTHETIC_BEARER_789", result)
        self.assertNotIn("SYNTHETIC_HEADER_ABC", result)
        self.assertIn("REDACTED", result)

    def test_redacts_explicit_known_secrets(self):
        result = redact_secrets(
            "Authentication failed for SYNTHETIC_CONFIG_SECRET",
            secrets=["SYNTHETIC_CONFIG_SECRET"],
        )

        self.assertNotIn("SYNTHETIC_CONFIG_SECRET", result)
        self.assertIn("REDACTED", result)

    def test_preserves_non_secret_diagnostics(self):
        message = "Provider timeout after 10 seconds for EURUSD M5"
        self.assertEqual(redact_secrets(message), message)

    def test_redaction_is_idempotent(self):
        message = "Request failed with apikey=SYNTHETIC_SECRET_999"
        once = redact_secrets(message)
        twice = redact_secrets(once)
        self.assertEqual(once, twice)


if __name__ == "__main__":
    unittest.main()
