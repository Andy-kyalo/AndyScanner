from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.stages.provider_stage import ProviderStage
from backend.providers.api_provider import APIProvider
from backend.provider_exceptions import ProviderConnectionError


# ==================================================
# Fake API failure
# ==================================================

def failing_request(
    self,
    url,
    api_key=None,
    limit=100,
):

    print("FAKE API FAILURE")

    raise ProviderConnectionError(
        "Simulated API connection failure."
    )


# ==================================================
# Create Context
# ==================================================

context = PipelineContext()

context.start(
    "US30",
    "M5",
)

context.set_metadata(
    "data_source",
    "API",
)

context.set_metadata(
    "api_url",
    "https://example.com/market-data",
)

context.set_metadata(
    "api_key",
    "TEST_KEY",
)

context.set_metadata(
    "provider_priority",
    [
        "API",
        "CSV",
        "MT5",
    ],
)


# ==================================================
# Create Provider Stage
# ==================================================

stage = ProviderStage()


# ==================================================
# Force API Failure
# ==================================================

original_request = APIProvider.request

APIProvider.request = failing_request


try:

    context = stage.run(
        context
    )

finally:

    APIProvider.request = original_request


# ==================================================
# Results
# ==================================================

print(
    "\n=== PROVIDER RECOVERY + FAILOVER TEST ==="
)

print(
    "Selected:",
    context.get_metadata(
        "selected_provider"
    ),
)

print(
    "Attempts:",
    context.get_metadata(
        "provider_attempts"
    ),
)

print(
    "Failures:",
    context.get_metadata(
        "provider_failures"
    ),
)

print(
    "Failover used:",
    context.get_metadata(
        "failover_used"
    ),
)

print(
    "Provider health:",
    context.get_metadata(
        "provider_health"
    ),
)

print(
    "Recovery:",
    context.get_metadata(
        "provider_recovery"
    ),
)

print(
    "Health checked:",
    context.get_metadata(
        "health_checked"
    ),
)

print(
    "Candles:",
    len(context.candles),
)


# ==================================================
# Assertions
# ==================================================

assert (
    context.get_metadata(
        "selected_provider"
    )
    == "CSVProvider"
)

assert (
    context.get_metadata(
        "provider_attempts"
    )
    == [
        "API",
        "CSV",
    ]
)

assert (
    context.get_metadata(
        "failover_used"
    )
    is True
)

assert (
    len(context.candles)
    == 4
)

assert (
    context.get_metadata(
        "health_checked"
    )
    is True
)


print(
    "\nPASS: Provider recovery + "
    "failover integration works."
)
