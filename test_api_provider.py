from backend.register_providers import register_providers
from backend.provider_factory import ProviderFactory
from backend.scanner_config import ScannerConfig


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


class FakeSession:
    def get(self, url, params=None, timeout=None):
        print("FAKE HTTP GET")
        print("URL:", url)
        print("Params:", params)
        print("Timeout:", timeout)

        return FakeResponse()


manager = register_providers()

config = ScannerConfig(
    market="US30",
    timeframe="M5",
    data_source="API",
)

factory = ProviderFactory(manager)

provider = factory.create(config)

provider.pool.acquire = lambda: FakeSession()
provider.pool.release = lambda session: None

raw_data = provider.request(
    url="https://example.com/market-data",
    api_key="TEST_KEY",
    limit=2,
)

print("\nRAW API DATA:")
print(raw_data)

candles = provider.map_candles(
    raw_data["data"]
)

print("\nMAPPED CANDLES:")
print("Count:", len(candles))

for candle in candles:
    print(
        candle.time,
        candle.open,
        candle.high,
        candle.low,
        candle.close,
        candle.get_type(),
    )
