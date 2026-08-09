from backend.api_error import APIError


error = APIError(
    code=429,
    message="Rate limit exceeded.",
    details="Too many requests.",
)

print("=== API ERROR MODEL TEST ===")

print("Code:", error.code)
print("Message:", error.message)
print("Details:", error.details)
print("Timestamp:", error.timestamp)

print("\nDictionary:")
print(error.to_dict())

print("\nString:")
print(str(error))

print("\nRepresentation:")
print(repr(error))
