from backend.validation.validators.invalid_prices import InvalidPricesValidator


class Candle:
    def __init__(self, time, open_, high, low, close):
        self.time = time
        self.open = open_
        self.high = high
        self.low = low
        self.close = close


validator = InvalidPricesValidator()

valid = [
    Candle("10:00", 100, 110, 95, 105),
    Candle("10:05", 105, 115, 100, 112),
]

invalid = [
    Candle("10:00", 100, 90, 95, 105),
]

print(validator.validate(valid))
print(validator.validate(invalid))