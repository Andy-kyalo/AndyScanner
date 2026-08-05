from backend.validation.validators.timeframe_validator import TimeframeValidator


class Candle:
    def __init__(self, time):
        self.time = time


validator = TimeframeValidator("M5")

valid = [
    Candle("10:00"),
    Candle("10:05"),
    Candle("10:10"),
    Candle("10:15"),
]

invalid = [
    Candle("10:00"),
    Candle("10:03"),
    Candle("10:10"),
]

print(validator.validate(valid))
print(validator.validate(invalid))