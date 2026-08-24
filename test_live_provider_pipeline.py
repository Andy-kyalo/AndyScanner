"""
test_live_provider_pipeline.py

Integration tests for the Twelve Data -> ProviderStage pipeline.

These tests use mocked HTTP responses.
No real Twelve Data API calls are made.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from unittest.mock import patch

from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.stages.provider_stage import ProviderStage
from backend.provider_exceptions import (
    ProviderDataError,
    ProviderRateLimitError,
    ProviderTimeoutError,
)
from backend.register_providers import register_providers


# ==========================================================
# Fake HTTP Response
# ==========================================================

class FakeResponse:

    def __init__(
        self,
        status_code=200,
        data=None,
    ):
        self.status_code = status_code
        self._data = data

    def json(self):
        return self._data


# ==========================================================
# Twelve Data Payload
# ==========================================================

VALID_PAYLOAD = {
    "status": "ok",
    "values": [
        {
            "datetime": "2026-08-23 18:15:00",
            "open": "1.1700",
            "high": "1.1710",
            "low": "1.1690",
            "close": "1.1705",
        },
        {
            "datetime": "2026-08-23 18:20:00",
            "open": "1.1705",
            "high": "1.1720",
            "low": "1.1700",
            "close": "1.1715",
        },
        {
            "datetime": "2026-08-23 18:25:00",
            "open": "1.1715",
            "high": "1.1730",
            "low": "1.1710",
            "close": "1.1725",
        },
        {
            "datetime": "2026-08-23 18:30:00",
            "open": "1.1725",
            "high": "1.1740",
            "low": "1.1720",
            "close": "1.1735",
        },
    ],
}


# ==========================================================
# Context
# ==========================================================

def make_context():

    register_providers()

    context = PipelineContext()

    context.start(
        "EURUSD",
        "M5",
    )

    context.set_metadata(
        "data_source",
        "TWELVEDATA",
    )

    context.set_metadata(
        "api_url",
        "https://api.twelvedata.com/time_series",
    )

    context.set_metadata(
        "api_key",
        "TEST_KEY",
    )

    context.set_metadata(
        "provider_priority",
        [
            "TWELVEDATA",
            "CSV",
            "MT5",
        ],
    )

    return context


# ==========================================================
# Success
# ==========================================================

@patch(
    "backend.providers.twelvedata_provider.requests.get"
)
def test_twelvedata_success_reaches_pipeline(mock_get):

    mock_get.return_value = FakeResponse(
        status_code=200,
        data=VALID_PAYLOAD,
    )

    context = make_context()

    context = ProviderStage().run(
        context
    )

    selected = context.get_metadata(
        "selected_provider"
    )

    candles = context.candles

    assert selected is not None
    assert selected == "TwelveDataProvider"

    assert len(candles) == 4

    assert context.get_metadata(
        "failover_used"
    ) is False


# ==========================================================
# Timeout
# ==========================================================

@patch(
    "backend.providers.twelvedata_provider.requests.get"
)
def test_twelvedata_timeout_fails_cleanly(mock_get):

    mock_get.side_effect = ProviderTimeoutError(
        "Simulated Twelve Data timeout."
    )

    context = make_context()

    try:
        ProviderStage().run(context)

    except Exception as error:

        assert isinstance(
            error,
            ProviderTimeoutError,
        )

        assert context.get_metadata(
            "selected_provider"
        ) is None

    else:

        raise AssertionError(
            "Expected Twelve Data timeout failure."
        )


# ==========================================================
# Rate Limit
# ==========================================================

@patch(
    "backend.providers.twelvedata_provider.requests.get"
)
def test_twelvedata_rate_limit_fails_cleanly(mock_get):

    mock_get.return_value = FakeResponse(
        status_code=429,
        data={
            "status": "error",
            "message": "Rate limit exceeded.",
        },
    )

    context = make_context()

    try:
        ProviderStage().run(context)

    except Exception as error:

        assert isinstance(
            error,
            ProviderRateLimitError,
        )

        assert context.get_metadata(
            "selected_provider"
        ) is None

    else:

        raise AssertionError(
            "Expected Twelve Data rate-limit failure."
        )


# ==========================================================
# Malformed Data
# ==========================================================

@patch(
    "backend.providers.twelvedata_provider.requests.get"
)
def test_twelvedata_malformed_data_is_rejected(mock_get):

    mock_get.return_value = FakeResponse(
        status_code=200,
        data={
            "status": "ok",
            "values": [
                {
                    "datetime": "2026-08-23 18:15:00",
                    "open": "INVALID",
                    "high": "1.1710",
                    "low": "1.1690",
                    "close": "1.1705",
                }
            ],
        },
    )

    context = make_context()

    try:
        ProviderStage().run(context)

    except Exception as error:

        assert isinstance(
            error,
            ProviderDataError,
        )

        assert context.get_metadata(
            "selected_provider"
        ) is None

    else:

        raise AssertionError(
            "Expected malformed market data to be rejected."
        )


# ==========================================================
# Runner
# ==========================================================

TESTS = [
    test_twelvedata_success_reaches_pipeline,
    test_twelvedata_timeout_fails_cleanly,
    test_twelvedata_rate_limit_fails_cleanly,
    test_twelvedata_malformed_data_is_rejected,
]


if __name__ == "__main__":

    print(
        "\n=== TWELVE DATA PIPELINE INTEGRATION TEST ==="
    )

    passed = 0

    for test in TESTS:

        try:

            test()

            print(
                f"PASS: {test.__name__}"
            )

            passed += 1

        except Exception as error:

            print(
                f"FAIL: {test.__name__}"
            )

            print(
                f"      {type(error).__name__}: {error}"
            )

            raise

    print()

    print(
        f"PASS: Twelve Data pipeline integration verified."
    )

    print(
        f"Tests passed: {passed}/{len(TESTS)}"
    )
