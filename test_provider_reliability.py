
from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.stages.provider_stage import ProviderStage
from backend.providers.api_provider import APIProvider
from backend.provider_exceptions import ProviderConnectionError


# ==================================================
# Fake API Failure
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
# Create Pipeline Context
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
# Collect Results
# ==================================================

selected = context.get_metadata(
    "selected_provider"
)

attempts = context.get_metadata(
    "provider_attempts"
)

failures = context.get_metadata(
    "provider_failures"
)

health = context.get_metadata(
    "provider_health"
)

recovery = context.get_metadata(
    "provider_recovery"
)

failover_used = context.get_metadata(
    "failover_used"
)

health_checked = context.get_metadata(
    "health_checked"
)


# ==================================================
# Reliability Report
# ==================================================

print(
    "\n=== PROVIDER RELIABILITY TEST ==="
)

print(
    "Selected provider:",
    selected
)

print(
    "Provider attempts:",
    attempts
)

print(
    "Provider failures:",
    failures
)

print(
    "Provider health:",
    health
)

print(
    "Provider recovery:",
    recovery
)

print(
    "Failover used:",
    failover_used
)

print(
    "Health checked:",
    health_checked
)

print(
    "Candles:",
    len(context.candles)
)


# ==================================================
# Assertions
# ==================================================

assert selected == "CSVProvider"

assert attempts == [
    "API",
    "CSV",
]

assert failover_used is True

assert health_checked is True

assert health["API"] is False

assert health["CSV"] is True

assert (
    recovery["API"]["status"]
    == "COOLDOWN"
)

assert (
    recovery["API"]["recovery_attempts"]
    == 1
)

assert (
    recovery["CSV"]["status"]
    == "AVAILABLE"
)

assert (
    len(context.candles)
    == 4
)


# ==================================================
# Reliability Summary
# ==================================================

print(
    "\n=== RELIABILITY SUMMARY ==="
)

print(
    "Health system: PASS"
)

print(
    "Recovery system: PASS"
)

print(
    "Cooldown system: PASS"
)

print(
    "Failover system: PASS"
)

print(
    "Market data loading: PASS"
)

print(
    "Pipeline metadata: PASS"
)

print(
    "\nPASS: Complete provider reliability "
    "integration works."
)
