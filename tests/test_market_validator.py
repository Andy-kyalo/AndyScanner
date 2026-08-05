from backend.validation.market_validator import MarketValidator


class Candle:
    def __init__(self, time, open_, high, low, close):
        self.time = time
        self.open = open_
        self.high = high
        self.low = low
        self.close = close


validator = MarketValidator()

# -------------------------------
# VALID DATA
# -------------------------------

valid = [

    Candle("10:00", 100, 110, 95, 105),

    Candle("10:05", 105, 115, 100, 112),

    Candle("10:10", 112, 118, 110, 117),

]

print(validator.validate(valid))

# -------------------------------
# DUPLICATE TIME
# -------------------------------

duplicate = [

    Candle("10:00", 100, 110, 95, 105),

    Candle("10:00", 105, 115, 100, 112),

    Candle("10:10", 112, 118, 110, 117),

]

print(validator.validate(duplicate))

# -------------------------------
# INVALID PRICES
# -------------------------------

bad_price = [

    Candle("10:00", 100, 90, 95, 105),

    Candle("10:05", 105, 115, 100, 112),

    Candle("10:10", 112, 118, 110, 117),

]

print(validator.validate(bad_price))

# -------------------------------
# BAD TIMEFRAME
# -------------------------------

bad_timeframe = [

    Candle("10:00", 100, 110, 95, 105),

    Candle("10:03", 105, 115, 100, 112),

    Candle("10:10", 112, 118, 110, 117),

]

print(validator.validate(bad_timeframe))