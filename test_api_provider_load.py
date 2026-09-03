from backend.register_providers import register_providers
from backend.provider_factory import ProviderFactory
from backend.scanner_config import ScannerConfig


# ==========================================
# Fake API response
# ==========================================

fake_api_response = {
    "status": "ok",
    "values": [
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


# ==========================================
# Provider setup
# ==========================================

manager = register_providers()

config = ScannerConfig(
    market="US30",
    timeframe="M5",
    data_source="API",
    api_url="https://example.com/market-data",
    api_key="TEST_KEY",
)

factory = ProviderFactory(manager)

provider = factory.create(config)


# ==========================================
# Replace request() with fake API
# ==========================================

def fake_request(
    url,
    symbol=None,
    api_key=None,
    limit=100,
    ):
    print("FAKE API REQUEST")
    print("URL:", url)
    print("API KEY:", api_key)
    print("LIMIT:", limit)

    return fake_api_response


provider.request = fake_request


# ==========================================
# Test load()
# ==========================================

candles = provider.load()


print("\n=== API PROVIDER LOAD TEST ===")
print("Provider:", type(provider).__name__)
print("Mapper:", type(provider.mapper).__name__)
print("Candles:", len(candles))


for candle in candles:
    print(
        candle.time,
        candle.open,
        candle.high,
        candle.low,
        candle.close,
        candle.get_type(),
    )


# ==========================================
# Assertions
# ==========================================

assert len(candles) == 2

assert candles[0].open == 100.0
assert candles[0].close == 103.0

assert candles[1].open == 103.0
assert candles[1].close == 106.0

assert candles[0].get_type() == "Bullish"
assert candles[1].get_type() == "Bullish"

print("\nPASS: APIProvider.load() completed successfully.")
print("PASS: API response reached Candle objects.")
