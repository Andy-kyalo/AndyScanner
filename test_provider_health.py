from backend.provider_health import ProviderHealth


# ==================================================
# Fake provider
# ==================================================

class FakeProvider:

    name = "FakeProvider"

    def __init__(self, should_fail=False):

        self.should_fail = should_fail
        self.calls = 0
    def probe(self):
        return not self.should_fail

    def load(self):

        self.calls += 1

        if self.should_fail:

            raise ConnectionError(
                "Simulated provider failure."
            )

        return [
            {
                "time": "2026-08-09 14:00:00",
                "open": 100.0,
                "high": 105.0,
                "low": 98.0,
                "close": 103.0,
            }
        ]


# ==================================================
# Healthy provider
# ==================================================

provider = FakeProvider()

health = ProviderHealth(provider)

print("=== PROVIDER HEALTH TEST ===")

print("Initial status:", health.status)

result = health.check()

print("Check result:", result)
print("Status:", health.status)

print("\nReport:")

for key, value in health.report().items():

    print(f"{key}: {value}")


assert result is True
assert health.healthy is True
assert health.status == "HEALTHY"
assert health.total_checks == 1
assert health.successful_checks == 1
assert health.failed_checks == 0
assert health.consecutive_failures == 0


# ==================================================
# Failed provider
# ==================================================

failed_provider = FakeProvider(
    should_fail=True
)

failed_health = ProviderHealth(
    failed_provider
)

result = failed_health.check()

print("\n=== FAILURE TEST ===")

print("Check result:", result)
print("Status:", failed_health.status)
print(
    "Consecutive failures:",
    failed_health.consecutive_failures
)
print(
    "Last error:",
    failed_health.last_error
)

assert result is False
assert failed_health.healthy is False
assert failed_health.status == "UNHEALTHY"
assert failed_health.total_checks == 1
assert failed_health.successful_checks == 0
assert failed_health.failed_checks == 1
assert failed_health.consecutive_failures == 1


print("\nPASS: ProviderHealth tracking works.")
