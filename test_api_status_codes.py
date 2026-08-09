from backend.api_response_handler import APIResponseHandler
from backend.api_error import APIError


class FakeResponse:
    def __init__(self, status_code):
        self.status_code = status_code
        self.text = f"HTTP error {status_code}"

    def json(self):
        return {"status": "error"}


status_codes = [400, 401, 403, 404, 429, 500]

print("=== API STATUS CODE TESTS ===")

for status_code in status_codes:

    response = FakeResponse(status_code)

    try:
        APIResponseHandler.parse(response)

        print(
            f"FAIL: HTTP {status_code} was accepted."
        )

    except APIError as error:

        print(
            f"PASS: HTTP {status_code} rejected "
            f"→ {error}"
        )
