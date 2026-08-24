from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.stages.provider_stage import ProviderStage
from backend.provider_exceptions import ProviderConnectionError
from backend.register_providers import register_providers


# ==================================================
# Fake Provider That Always Fails During Load
# ==================================================

class AlwaysFailProvider:

    def __init__(self, config, name):
        self.config = config
        self.name = name

    def probe(self):
        # Health check must pass.
        return True

    def load(self, symbol=None):
        # Actual market-data request fails.
        raise ProviderConnectionError(
            f"Simulated {self.name} connection failure."
        )


class FailingAPIProvider:

    name = "APIProvider"

    def __init__(self, config):
        self.config = config

    def probe(self):
        return True

    def load(self, symbol=None):
        raise ProviderConnectionError(
            "Simulated API connection failure."
        )


class FailingCSVProvider:

    name = "CSVProvider"

    def __init__(self, config):
        self.config = config

    def probe(self):
        return True

    def load(self, symbol=None):
        raise ProviderConnectionError(
            "Simulated CSV connection failure."
        )


# ==================================================
# Register Fake Providers
# ==================================================

provider_manager = register_providers()

original_api = provider_manager.get_provider("API")
original_csv = provider_manager.get_provider("CSV")

provider_manager.register(
    "API",
    FailingAPIProvider,
)

provider_manager.register(
    "CSV",
    FailingCSVProvider,
)


# ==================================================
# Pipeline Context
# ==================================================

context = PipelineContext()

context.start(
    "EURUSD",
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
# Run Provider Stage
# ==================================================

stage = ProviderStage()

final_error = None

try:

    stage.run(context)

except Exception as error:

    final_error = error

finally:

    # Always restore real providers.
    provider_manager.register(
        "API",
        original_api,
    )

    provider_manager.register(
        "CSV",
        original_csv,
    )


# ==================================================
# Results
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


print(
    "\n=== ALL-PROVIDERS-FAIL TEST ==="
)

print(
    "Selected provider:",
    selected,
)

print(
    "Provider attempts:",
    attempts,
)

print(
    "Provider failures:",
    failures,
)

print(
    "Provider health:",
    health,
)

print(
    "Provider recovery:",
    recovery,
)

print(
    "Failover used:",
    failover_used,
)

print(
    "Health checked:",
    health_checked,
)

print(
    "Final error:",
    type(final_error).__name__
    if final_error
    else None,
)

print(
    "Final message:",
    str(final_error)
    if final_error
    else None,
)


# ==================================================
# Assertions
# ==================================================

# No provider may be selected.
assert selected is None

# API and CSV must have been attempted.
assert "API" in attempts
assert "CSV" in attempts

# Failover must have occurred.
assert failover_used is True

# Health system must have run.
assert health_checked is True

# Both fake providers passed health checks
# before their actual loads failed.
assert health["API"] is True
assert health["CSV"] is True

# Both providers must enter cooldown after
# their actual connection failures.
assert recovery["API"]["status"] == "COOLDOWN"
assert recovery["CSV"]["status"] == "COOLDOWN"

# We must have recorded failures for both.
api_failures = [
    failure
    for failure in failures
    if failure.get("provider") == "API"
]

csv_failures = [
    failure
    for failure in failures
    if failure.get("provider") == "CSV"
]

assert api_failures
assert csv_failures

# The actual load failures must be classified
# as connection failures.
assert api_failures[-1]["category"] == "CONNECTION_ERROR"
assert csv_failures[-1]["category"] == "CONNECTION_ERROR"

# The pipeline must fail cleanly because no provider
# was able to supply candles.
assert final_error is not None


print(
    "\nPASS: All-providers-fail behavior works."
)
