from backend.api_response_handler import APIResponseHandler


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
                }
            ],
        }


response = FakeResponse()

print("VALIDATE:")
print(APIResponseHandler.validate(response))

print("\nPARSE:")
print(APIResponseHandler.parse(response))
