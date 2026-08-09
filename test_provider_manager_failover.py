from backend.register_providers import register_providers
from backend.provider_manager import ProviderManager
from backend.scanner_config import ScannerConfig


manager = register_providers()

config = ScannerConfig(
    market="US30",
    timeframe="M5",
    data_source="API",
)


print("=== PROVIDER MANAGER SPECIFIC PROVIDER TEST ===")

api_provider = manager.create_provider(
    "API",
    config,
)

csv_provider = manager.create_provider(
    "CSV",
    config,
)

mt5_provider = manager.create_provider(
    "MT5",
    config,
)

print("API:", type(api_provider).__name__)
print("CSV:", type(csv_provider).__name__)
print("MT5:", type(mt5_provider).__name__)

print("\nMetrics:")
print(manager.metrics_report())

print("\nPASS: Manager can create specific providers.")
