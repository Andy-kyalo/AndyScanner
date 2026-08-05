from backend.validation.validators.empty_response import (
    EmptyResponseValidator
)

validator = EmptyResponseValidator()

print(validator.validate(None))

print(validator.validate([]))

print(validator.validate([1, 2, 3]))