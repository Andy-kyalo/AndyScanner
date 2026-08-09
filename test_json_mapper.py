from backend.mapping.json_mapper import JSONMapper
from backend.candle import Candle


raw_data = [
    {
        "time": "2026-08-09 14:00:00",
        "open": 100.0,
        "high": 105.0,
        "low": 98.0,
        "close": 103.0,
    },
    {
        "time": "2026-08-09 14:05:00",
        "open": 103.0,
        "high": 108.0,
        "low": 101.0,
        "close": 106.0,
    },
]


mapper = JSONMapper()

candles = mapper.map(raw_data)

print("Mapped candles:", len(candles))

for index, candle in enumerate(candles, start=1):

    print(f"\nCandle {index}")

    print("Class:", candle.__class__.__name__)
    print("Time:", candle.time)
    print("Open:", candle.open)
    print("High:", candle.high)
    print("Low:", candle.low)
    print("Close:", candle.close)
    print("Type:", candle.get_type())
    print("Body:", candle.body_size())
    print("Range:", candle.range())
