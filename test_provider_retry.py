from backend.provider_retry import ProviderRetry
from backend.provider_exceptions import ProviderConnectionError


print("=== PROVIDER RETRY TEST ===")


attempts = {
    "count": 0,
}


def failing_operation():

    attempts["count"] += 1

    print(
        f"Attempt {attempts['count']}"
    )

    raise ProviderConnectionError(
        "Test connection failure."
    )


retry = ProviderRetry(
    retries=3,
    delay=0,
)


try:

    retry.execute(
        failing_operation
    )

except ProviderConnectionError as error:

    print(
        "\nPASS: Retry exhausted."
    )

    print(
        "Attempts:",
        attempts["count"],
    )

    print(
        "Error:",
        error,
    )
