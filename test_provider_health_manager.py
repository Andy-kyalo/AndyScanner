from backend.provider_manager import ProviderManager
from backend.provider_health_manager import ProviderHealthManager


# ==================================================
# Fake Providers
# ==================================================

class HealthyProvider:

    name = "HealthyProvider"

    def __init__(self, config):
        self.config = config
        self.calls = 0

    def probe(self):
        """
        Healthy provider passes the readiness check.
        """
        return True

    def load(self):

        self.calls += 1

        return [
            {
                "time": "2026-08-09 14:00:00",
                "open": 100.0,
                "high": 105.0,
                "low": 98.0,
                "close": 103.0,
            }
        ]


class FailingProvider:

    name = "FailingProvider"

    def __init__(self, config):
        self.config = config
        self.calls = 0

    def probe(self):
        """
        Failing provider fails the readiness check.
        """
        return False

    def load(self):

        self.calls += 1

        raise ConnectionError(
            "Simulated provider failure."
        )


# ==================================================
# Provider Manager
# ==================================================

manager = ProviderManager()

manager.register(
    "HEALTHY",
    HealthyProvider,
)

manager.register(
    "FAILING",
    FailingProvider,
)


# ==================================================
# Health Manager
# ==================================================

health_manager = ProviderHealthManager(
    manager
)


print("=== PROVIDER HEALTH MANAGER TEST ===")


# ==================================================
# Healthy Provider Test
# ==================================================

result = health_manager.check(
    "HEALTHY"
)

print(
    "Healthy provider result:",
    result,
)

assert result is True

assert health_manager.is_healthy(
    "HEALTHY"
) is True


# ==================================================
# Failing Provider Test
# ==================================================

result = health_manager.check(
    "FAILING"
)

print(
    "Failing provider result:",
    result,
)

assert result is False

assert health_manager.is_healthy(
    "FAILING"
) is False


# ==================================================
# Report
# ==================================================

print("\nHealth Report:")

for provider, report in (
    health_manager.report().items()
):

    print(
        provider,
        "=>",
        report,
    )


# ==================================================
# Check All
# ==================================================

results = health_manager.check_all()

print("\nCheck All:")

print(results)

assert results["HEALTHY"] is True

assert results["FAILING"] is False


print(
    "\nPASS: ProviderHealthManager works."
)