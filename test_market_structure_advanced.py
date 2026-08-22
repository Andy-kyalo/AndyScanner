from backend.candle import Candle
from backend.market_structure_engine import MarketStructureEngine


# ============================================================
# HELPERS
# ============================================================

def c(time, o, h, l, cl):
    return Candle(time, o, h, l, cl)


def section(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def check(condition, message):
    if not condition:
        raise AssertionError(message)

    print(f"PASS: {message}")


def show_engine(engine):
    print()
    print("SWING HIGHS:")
    for point in engine.swing_highs():
        print(" ", point)

    print()
    print("SWING LOWS:")
    for point in engine.swing_lows():
        print(" ", point)

    print()
    print("EVENTS:")
    for event in engine.events():
        print(" ", event)

    print()
    print("TREND           :", engine.trend())
    print("STRUCTURAL STATE:", engine.structural_state())
    print("STRUCTURE       :", engine.structure())
    print("CURRENT EVENT   :", engine.current_event())
    print("PROTECTED HIGH  :", engine.protected_high())
    print("PROTECTED LOW   :", engine.protected_low())


# ============================================================
# TEST 1 — BULLISH STRUCTURAL BREAK
# ============================================================

section("TEST 1 — BULLISH STRUCTURAL BREAK")

candles = [
    c("2026-01-01 00:00:00", 100, 101, 99, 100),
    c("2026-01-01 00:05:00", 100, 105, 99, 104),
    c("2026-01-01 00:10:00", 104, 106, 98, 99),
    c("2026-01-01 00:15:00", 99, 102, 97, 101),

    # Close strictly above 106.
    c("2026-01-01 00:20:00", 101, 108, 100, 107),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

event = engine.current_event()

check(
    event is not None,
    "Bullish structural event exists.",
)

check(
    event.event == "STRUCTURE_BREAK",
    "First bullish break is STRUCTURE_BREAK.",
)

check(
    event.direction == "BULLISH",
    "Structural break direction is bullish.",
)

check(
    event.index == 4,
    "Bullish break occurs at index 4.",
)

check(
    event.level == 106,
    "Bullish break occurs through level 106.",
)

check(
    engine.structural_state() == "BULLISH",
    "Bullish structural state is established.",
)


# ============================================================
# TEST 2 — WICK BREAK MUST NOT CONFIRM
# ============================================================

section("TEST 2 — WICK BREAK WITHOUT CLOSE")

candles = [
    c("2026-01-02 00:00:00", 100, 101, 99, 100),
    c("2026-01-02 00:05:00", 100, 105, 99, 104),
    c("2026-01-02 00:10:00", 104, 106, 98, 99),
    c("2026-01-02 00:15:00", 99, 102, 97, 101),

    # Wick reaches above 106,
    # but close remains below 106.
    c("2026-01-02 00:20:00", 101, 107, 100, 105),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

check(
    engine.current_event() is None,
    "Wick above structural level does not confirm a break.",
)


# ============================================================
# TEST 3 — EXACT LEVEL IS NOT A BREAK
# ============================================================

section("TEST 3 — EXACT LEVEL")

candles = [
    c("2026-01-03 00:00:00", 100, 101, 99, 100),
    c("2026-01-03 00:05:00", 100, 105, 99, 104),
    c("2026-01-03 00:10:00", 104, 106, 98, 99),
    c("2026-01-03 00:15:00", 99, 102, 97, 101),

    # Close exactly at 106.
    c("2026-01-03 00:20:00", 101, 106, 100, 106),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

check(
    engine.current_event() is None,
    "Close exactly at structural level does not confirm a break.",
)


# ============================================================
# TEST 4 — NO DUPLICATE BREAK
# ============================================================

section("TEST 4 — NO DUPLICATE BREAK")

candles = [
    c("2026-01-04 00:00:00", 100, 101, 99, 100),
    c("2026-01-04 00:05:00", 100, 105, 99, 104),
    c("2026-01-04 00:10:00", 104, 106, 98, 99),
    c("2026-01-04 00:15:00", 99, 102, 97, 101),

    # First confirmed break.
    c("2026-01-04 00:20:00", 101, 108, 100, 107),

    # Price remains above the broken level.
    c("2026-01-04 00:25:00", 107, 109, 105, 108),
    c("2026-01-04 00:30:00", 108, 110, 106, 109),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

bullish_events = [
    event
    for event in engine.events()
    if event.direction == "BULLISH"
]

check(
    len(bullish_events) == 1,
    "The same structural level produces only one bullish event.",
)


# ============================================================
# TEST 5 — MULTIPLE SWINGS + HH / HL
# ============================================================

section("TEST 5 — MULTIPLE SWINGS")

multiple_swing_candles = [
    # 0 — baseline
    c("2026-01-05 00:00:00", 100, 101, 99, 100),

    # 1 — rising
    c("2026-01-05 00:05:00", 100, 105, 99, 104),

    # 2 — HIGH #1 = 108
    c("2026-01-05 00:10:00", 104, 108, 102, 107),

    # 3 — LOW #1 = 97
    c("2026-01-05 00:15:00", 107, 107, 97, 99),

    # 4 — recovery, but NOT another structural high
    c("2026-01-05 00:20:00", 99, 104, 98, 103),

    # 5 — HIGH #2 = 110
    c("2026-01-05 00:25:00", 103, 110, 101, 108),

    # 6 — LOW #2 = 100
    c("2026-01-05 00:30:00", 108, 109, 100, 102),

    # 7 — recovery
    c("2026-01-05 00:35:00", 102, 108, 101, 107),

    # 8 — HIGH #3 = 114
    c("2026-01-05 00:40:00", 107, 114, 106, 112),

    # 9 — confirms HIGH #3
    c("2026-01-05 00:45:00", 112, 113, 104, 106),
]

multi_engine = MarketStructureEngine(
    multiple_swing_candles,
    swing_strength=1,
)

show_engine(multi_engine)

highs = multi_engine.swing_highs()
lows = multi_engine.swing_lows()

check(
    len(highs) >= 3,
    "At least three confirmed swing highs are detected.",
)

check(
    len(lows) >= 2,
    "At least two confirmed swing lows are detected.",
)

check(
    highs[0].price == 108,
    "First swing high is 108.",
)

check(
    highs[1].price == 110,
    "Second swing high is 110.",
)

check(
    highs[2].price == 114,
    "Third swing high is 114.",
)

check(
    lows[0].price == 97,
    "First swing low is 97.",
)

check(
    lows[1].price == 100,
    "Second swing low is 100.",
)

check(
    highs[1].label == "HH",
    "Second swing high is classified as HH.",
)

check(
    lows[1].label == "HL",
    "Second swing low is classified as HL.",
)

check(
    highs[2].label == "HH",
    "Third swing high is classified as HH.",
)


# ============================================================
# TEST 6 — NO LOOK-AHEAD
# ============================================================

section("TEST 6 — NO LOOK-AHEAD")

candles = [
    c("2026-01-06 00:00:00", 100, 101, 99, 100),
    c("2026-01-06 00:05:00", 100, 105, 99, 104),
    c("2026-01-06 00:10:00", 104, 106, 98, 99),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

highs = engine.swing_highs()
lows = engine.swing_lows()

for point in highs:
    check(
        point.index < len(candles) - 1,
        "Confirmed swing high is never the newest candle.",
    )

for point in lows:
    check(
        point.index < len(candles) - 1,
        "Confirmed swing low is never the newest candle.",
    )

check(
    all(point.index < len(candles) - 1 for point in highs + lows),
    "No swing is confirmed using unavailable future data.",
)


# ============================================================
# TEST 7 — STRICT CLOSE-THROUGH SEMANTICS
# ============================================================

section("TEST 7 — STRICT CLOSE-THROUGH")

# Close above level.
candles = [
    c("2026-01-07 00:00:00", 100, 101, 99, 100),
    c("2026-01-07 00:05:00", 100, 105, 99, 104),
    c("2026-01-07 00:10:00", 104, 106, 98, 99),
    c("2026-01-07 00:15:00", 99, 102, 97, 101),
    c("2026-01-07 00:20:00", 101, 108, 100, 107),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

check(
    engine.current_event() is not None,
    "Close strictly above the level confirms a break.",
)


# Close exactly at level.
candles = [
    c("2026-01-08 00:00:00", 100, 101, 99, 100),
    c("2026-01-08 00:05:00", 100, 105, 99, 104),
    c("2026-01-08 00:10:00", 104, 106, 98, 99),
    c("2026-01-08 00:15:00", 99, 102, 97, 101),
    c("2026-01-08 00:20:00", 101, 106, 100, 106),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

check(
    engine.current_event() is None,
    "Close exactly at the level does not confirm a break.",
)


# ============================================================
# TEST 8 — DETERMINISM
# ============================================================

section("TEST 8 — DETERMINISM")

# Use the richer multi-swing engine for deterministic testing.
engine = multi_engine

snapshot_1 = engine.snapshot()
snapshot_2 = engine.snapshot()

check(
    snapshot_1 == snapshot_2,
    "Snapshots remain deterministic.",
)

check(
    engine.events() == engine.events(),
    "Event history remains deterministic.",
)

check(
    engine.swing_highs() == engine.swing_highs(),
    "Swing highs remain deterministic.",
)

check(
    engine.swing_lows() == engine.swing_lows(),
    "Swing lows remain deterministic.",
)


# ============================================================
# TEST 9 — SNAPSHOT CONSISTENCY
# ============================================================

section("TEST 9 — SNAPSHOT CONSISTENCY")

snapshot = multi_engine.snapshot()

check(
    snapshot["swing_high_count"] == multi_engine.swing_high_count(),
    "Snapshot high count matches engine.",
)

check(
    snapshot["swing_low_count"] == multi_engine.swing_low_count(),
    "Snapshot low count matches engine.",
)

check(
    snapshot["event_count"] == len(multi_engine.events()),
    "Snapshot event count matches event history.",
)

check(
    snapshot["latest_high"]["price"] == multi_engine.latest_swing_high().price,
    "Snapshot latest high matches engine.",
)

check(
    snapshot["latest_low"]["price"] == multi_engine.latest_swing_low().price,
    "Snapshot latest low matches engine.",
)


# ============================================================
# FINAL RESULT
# ============================================================

section("FINAL RESULT")

print("ADVANCED MARKET STRUCTURE TESTS PASSED")
print()
print("Validated:")
print("  - structural break confirmation")
print("  - close-based break logic")
print("  - wick rejection")
print("  - exact-level rejection")
print("  - duplicate-break prevention")
print("  - multiple swing detection")
print("  - HH / HL classification")
print("  - no look-ahead")
print("  - strict close-through semantics")
print("  - deterministic calculations")
print("  - snapshot consistency")
print()
print("ADVANCED MARKET STRUCTURE ENGINE: PASS")