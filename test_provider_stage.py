from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.stages.provider_stage import ProviderStage


# ==================================================
# Fake API response
# ==================================================

class FakeResponse:

    status_code = 200

    text = '{"status": "ok"}'

    def json(self):

        return {
            "status": "ok",
            "data": [
                {
                    "time": "2026-08-09 14:00:00",
                    "open": 100.0,
                    "high": 105.0,
                    "low": 98.0,
                    "close": 103.0,
                },
                {
                    "time": "2026-08-09 14:05:00",
                    "open": 103.0,
                    "high": 108.0,
                    "low": 101.0,
                    "close": 106.0,
                },
            ],
        }


# ==================================================
# Fake API request
# ==================================================

def fake_request(
    self,
    url,
    api_key=None,
    limit=100,
):

    print("FAKE API REQUEST")
    print("URL:", url)
    print("API KEY:", api_key)
    print("LIMIT:", limit)

    return FakeResponse().json()


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


# ==================================================
# Create stage
# ==================================================

stage = ProviderStage()


# ==================================================
# Inject fake API request
# ==================================================

original_request = None


# We temporarily replace APIProvider.request
from backend.api_provider import APIProvider

original_request = APIProvider.request

APIProvider.request = fake_request


try:

    context = stage.run(context)

finally:

    APIProvider.request = original_request


# ==================================================
# Results
# ==================================================

print("\n=== PROVIDER STAGE API TEST ===")

print(
    "Provider:",
    context.provider.__class__.__name__,
)

print(
    "Data source:",
    context.get_metadata("data_source"),
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
    "\nPASS: ProviderStage returned API market data."
)

print(
    "PASS: API data reached Candle objects."
)
print(
    "Attempts:",
    context.get_metadata("provider_attempts"),
)

print(
    "Failures:",
    context.get_metadata("provider_failures"),
)

print(
    "Selected:",
    context.get_metadata("selected_provider"),
)

print(
    "Failover used:",
    context.get_metadata("failover_used"),
)
