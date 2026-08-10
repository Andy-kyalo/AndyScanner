from backend.provider_recovery import ProviderRecovery


# ==================================================
# Create recovery manager
# ==================================================

recovery = ProviderRecovery(
    cooldown=2.0,
)


print("=== PROVIDER RECOVERY TEST ===")


# ==================================================
# Initial state
# ==================================================

print(
    "Initial status:",
    recovery.status("API"),
)

assert recovery.status("API") == "AVAILABLE"
assert recovery.is_in_cooldown("API") is False


# ==================================================
# Record failure
# ==================================================

recovery.record_failure("API")

print(
    "After failure:",
    recovery.status("API"),
)

print(
    "Cooldown remaining:",
    recovery.cooldown_remaining("API"),
)

assert recovery.is_in_cooldown("API") is True
assert recovery.status("API") == "COOLDOWN"


# ==================================================
# Recovery attempt
# ==================================================

recovery.record_recovery_attempt("API")

print(
    "Recovery attempts:",
    recovery.recovery_attempts("API"),
)

assert recovery.recovery_attempts("API") == 1


# ==================================================
# Provider still unavailable
# ==================================================

print(
    "Can recover immediately:",
    recovery.can_attempt_recovery("API"),
)

assert recovery.can_attempt_recovery("API") is False


# ==================================================
# Successful recovery
# ==================================================

recovery.record_recovery("API")

print(
    "After recovery:",
    recovery.status("API"),
)

assert recovery.status("API") == "AVAILABLE"
assert recovery.is_in_cooldown("API") is False


# ==================================================
# Report
# ==================================================

print("\nRecovery Report:")

print(
    recovery.report()
)

print(
    "\nPASS: ProviderRecovery works."
)
