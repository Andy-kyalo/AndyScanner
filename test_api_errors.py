from backend.api_response_handler import APIResponseHandler
from backend.api_error import APIError


class FakeResponse:
    def __init__(self, status_code, data=None, text=""):
        self.status_code = status_code
        self._data = data
        self.text = text

    def json(self):
        if isinstance(self._data, Exception):
            raise self._data

        return self._data


def test_status_error():
    response = FakeResponse(
        500,
        text="Internal Server Error",
    )

    try:
        APIResponseHandler.parse(response)
        print("FAIL: 500 response was accepted.")

    except APIError as error:
        print("PASS: 500 response rejected.")
        print(error)


def test_invalid_json():
    response = FakeResponse(
        200,
        data=ValueError("Invalid JSON"),
    )

    try:
        APIResponseHandler.parse(response)
        print("FAIL: Invalid JSON was accepted.")

    except APIError as error:
        print("PASS: Invalid JSON rejected.")
        print(error)


def test_none_response():
    try:
        APIResponseHandler.parse(None)
        print("FAIL: None response was accepted.")

    except APIError as error:
        print("PASS: None response rejected.")
        print(error)


print("=== API ERROR TESTS ===\n")

test_status_error()

print()

test_invalid_json()

print()

test_none_response()
