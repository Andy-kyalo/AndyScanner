from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.stages.provider_stage import ProviderStage
from backend.api_provider import APIProvider
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
# Create context
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
# Create stage
# ==================================================

stage = ProviderStage()


# ==================================================
# Replace API request temporarily
# ==================================================

original_request = APIProvider.request

APIProvider.request = failing_request


try:

    context = stage.run(context)

finally:

    APIProvider.request = original_request


# ==================================================
# Results
# ==================================================

print(
    "\n=== PROVIDER FAILOVER TEST ==="
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
    "Candles:",
    len(context.candles),
)

for candle in context.candles:

    print(
        candle.time,
        candle.open,
        candle.high,
        candle.low,
        candle.close,
        candle.get_type(),
    )


print(
    "\nPASS: Provider failover completed."
)
