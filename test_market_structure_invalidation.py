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

    print()
    print("BULLISH INVALIDATION :", engine.bullish_invalidation())
    print("BEARISH INVALIDATION :", engine.bearish_invalidation())

    print()
    print("LAST INVALIDATION:")
    print(" ", engine.last_invalidation())


# ============================================================
# TEST 1
# NO PROTECTED LEVEL
# ============================================================

section("TEST 1 — NO PROTECTED LEVEL")

candles = [
    c("2026-04-01 00:00:00", 100, 101, 99, 100),
    c("2026-04-01 00:05:00", 100, 101, 97, 98),
    c("2026-04-01 00:10:00", 98, 106, 97, 104),
    c("2026-04-01 00:15:00", 104, 105, 100, 102),
    c("2026-04-01 00:20:00", 102, 109, 101, 107),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

check(
    engine.structural_state() == "BULLISH",
    "Bullish structural state exists.",
)

check(
    engine.protected_low() is None,
    "No protected low exists with insufficient bullish structure.",
)

check(
    engine.bullish_invalidation() is False,
    "No bullish invalidation exists without a protected level.",
)

check(
    engine.bearish_invalidation() is False,
    "No bearish invalidation exists without a protected level.",
)

check(
    engine.last_invalidation() is None,
    "Last invalidation is None when no protected level exists.",
)


# ============================================================
# TEST 2
# BULLISH WICK THROUGH PROTECTED LOW
# ============================================================

section("TEST 2 — BULLISH PROTECTED LOW WICK")

candles = [
    # 0
    c("2026-04-02 00:00:00", 100, 101, 99, 100),

    # 1 — INITIAL LOW
    c("2026-04-02 00:05:00", 100, 101, 97, 98),

    # 2 — INITIAL HIGh
    c("2026-04-02 00:10:00", 98, 106, 98, 104),

    # 3 — CONFIRM INITIAL HIGH
    c("2026-04-02 00:15:00", 104, 105, 100, 102),

    # 4 — BULLISH STRUCTURAL BREAK
    c("2026-04-02 00:20:00", 102, 109, 101, 107),

    # 5 — PULLBACK
    c("2026-04-02 00:25:00", 107, 108, 102, 103),

    # 6 — HIGHER-LOW CANDIDATE
    c("2026-04-02 00:30:00", 103, 104, 100, 101),

    # 7 — CONFIRM HIGHER LOW
    # Its LOW is above 100, so candle 6 becomes a confirmed swing LOW.
    c("2026-04-02 00:35:00", 101, 106, 101, 105),

    # 8 — WICK BELOW PROTECTED LOW 100
    # LOW = 99
    # CLOSE = 103
    c("2026-04-02 00:40:00", 105, 107, 99, 103),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

protected_low = engine.protected_low()

check(
    protected_low is not None,
    "A bullish protected low exists.",
)

check(
    protected_low.price == 100,
    "Protected low is the confirmed structural low at 100.",
)

check(
    engine.bullish_invalidation() is False,
    "A wick below the protected low does not invalidate bullish structure.",
)

check(
    engine.last_invalidation() is None,
    "No invalidation event is created by a wick.",
)


# ============================================================
# TEST 3
# BULLISH EXACT CLOSE
# ============================================================

section("TEST 3 — BULLISH EXACT PROTECTED LOW CLOSE")

candles = [
    c("2026-04-03 00:00:00", 100, 101, 99, 100),

    # INITIAL LOW
    c("2026-04-03 00:05:00", 100, 101, 97, 98),

    # INITIAL HIGH
    c("2026-04-03 00:10:00", 98, 106, 98, 104),

    # CONFIRM HIGH
    c("2026-04-03 00:15:00", 104, 105, 100, 102),

    # BULLISH BREAK
    c("2026-04-03 00:20:00", 102, 109, 101, 107),

    # PULLBACK / HIGHER-LOW CANDIDATE
    c("2026-04-03 00:25:00", 107, 108, 100, 103),

    # CONFIRM HIGHER LOW
    c("2026-04-03 00:30:00", 103, 106, 101, 105),

    # CLOSE EXACTLY AT PROTECTED LOW
    c("2026-04-03 00:35:00", 105, 106, 100, 100),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

protected_low = engine.protected_low()

check(
    protected_low is not None,
    "A bullish protected low exists.",
)

check(
    engine.bullish_invalidation() is False,
    "A close exactly at the protected low does not invalidate bullish structure.",
)

check(
    engine.last_invalidation() is None,
    "Exact-level close does not create invalidation.",
)


# ============================================================
# TEST 4
# BULLISH CLOSE THROUGH PROTECTED LOW
# ============================================================

section("TEST 4 — BULLISH STRUCTURE INVALIDATION")

candles = [
    c("2026-04-04 00:00:00", 100, 101, 99, 100),

    # INITIAL LOW
    c("2026-04-04 00:05:00", 100, 101, 97, 98),

    # INITIAL HIGH
    c("2026-04-04 00:10:00", 98, 106, 98, 104),

    # CONFIRM INITIAL HIGH
    c("2026-04-04 00:15:00", 104, 105, 101, 102),

    # BULLISH STRUCTURAL BREAK
    c("2026-04-04 00:20:00", 102, 109, 101, 107),

    # PULLBACK
    c("2026-04-04 00:25:00", 107, 108, 102, 103),

    # HIGHER LOW
    c("2026-04-04 00:30:00", 103, 106, 100, 105),

    # CONFIRM HIGHER LOW
    c("2026-04-04 00:35:00", 105, 107, 101, 104),

    # CLOSE STRICTLY BELOW PROTECTED LOW = 100
    c("2026-04-04 00:40:00", 104, 105, 96, 98),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

invalidation = engine.last_invalidation()

check(
    invalidation is not None,
    "Bullish protected-level violation creates an invalidation event.",
)

check(
    invalidation.event == "STRUCTURE_INVALIDATION",
    "The event is classified as STRUCTURE_INVALIDATION.",
)

check(
    invalidation.direction == "BEARISH",
    "Bullish invalidation has BEARISH direction.",
)

check(
    invalidation.level == 100,
    "Invalidation occurs through the protected low at 100.",
)

check(
    invalidation.index == 8,
    "Invalidation occurs on the close-through candle.",
)

check(
    engine.bearish_invalidation(),
    "bearish_invalidation() correctly reports the invalidation.",
)


# ============================================================
# TEST 5
# BEARISH WICK THROUGH PROTECTED HIGH
# ============================================================

section("TEST 5 — BEARISH PROTECTED HIGH WICK")

candles = [
    c("2026-04-05 00:00:00", 100, 101, 99, 100),

    # INITIAL HIGH
    c("2026-04-05 00:05:00", 100, 106, 99, 104),

    # INITIAL LOW
    c("2026-04-05 00:10:00", 104, 105, 97, 99),

    # CONFIRM LOW
    c("2026-04-05 00:15:00", 99, 102, 98, 101),

    # BEARISH BREAK
    c("2026-04-05 00:20:00", 101, 102, 95, 96),

    # LOWER-HIGH CANDIDATE
    c("2026-04-05 00:25:00", 96, 101, 95, 100),

    # CONFIRM LH = protected high 103
    c("2026-04-05 00:30:00", 101, 103, 100,  102),

    # Wick above 103, close remains below
    # Wick above 103, close remains below
c("2026-04-05 00:35:00", 99, 102, 95, 101),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

protected_high = engine.protected_high()

check(
    protected_high is not None,
    "A bearish protected high exists.",
)

check(
    protected_high.price == 103,
    "Protected high is the confirmed lower high at 103.",
)

check(
    engine.bullish_invalidation() is False,
    "A wick above the protected high does not invalidate bearish structure.",
)

check(
    engine.last_invalidation() is None,
    "No invalidation event is created by a wick.",
)


# ============================================================
# TEST 6
# BEARISH EXACT CLOSE
# ============================================================

section("TEST 6 — BEARISH EXACT PROTECTED HIGH CLOSE")

candles = [
    c("2026-04-06 00:00:00", 100, 101, 99, 100),

    # INITIAL HIGH
    c("2026-04-06 00:05:00", 100, 106, 99, 104),

    # INITIAL LOW
    c("2026-04-06 00:10:00", 104, 105, 97, 99),

    # CONFIRM LOW
    c("2026-04-06 00:15:00", 99, 102, 98, 101),

    # BEARISH BREAK
    c("2026-04-06 00:20:00", 101, 102, 95, 96),

    # LOWER-HIGH CANDIDATE
    c("2026-04-06 00:25:00", 96, 101, 95, 100),

    # LH = 103
    c("2026-04-06 00:30:00", 100, 103, 98, 99),

    # CONFIRM LH — must be BELOW 103
    c("2026-04-06 00:35:00", 99, 102, 96, 100),

    # EXACT CLOSE AT PROTECTED HIGH
    c("2026-04-06 00:40:00", 100, 103, 98, 103),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

check(
    engine.protected_high() is not None,
    "A bearish protected high exists.",
)

check(
    engine.bullish_invalidation() is False,
    "A close exactly at the protected high does not invalidate bearish structure.",
)

check(
    engine.last_invalidation() is None,
    "Exact-level close does not create invalidation.",
)


# ============================================================
# TEST 7
# BEARISH CLOSE THROUGH PROTECTED HIGH
# ============================================================

section("TEST 7 — BEARISH STRUCTURE INVALIDATION")

candles = [
    c("2026-04-07 00:00:00", 100, 101, 99, 100),

    # INITIAL HIGH
    c("2026-04-07 00:05:00", 100, 106, 99, 104),

    # INITIAL LOW
    c("2026-04-07 00:10:00", 104, 105, 97, 99),

    # CONFIRM LOW
    c("2026-04-07 00:15:00", 99, 102, 98, 101),

    # BEARISH BREAK
    c("2026-04-07 00:20:00", 101, 102, 95, 96),

    # LOWER-HIGH CANDIDATE
    c("2026-04-07 00:25:00", 96, 101, 95, 100),

    # LOWER HIGH
    c("2026-04-07 00:30:00", 100, 103, 98, 99),

    # CONFIRM LH
    c("2026-04-07 00:35:00", 99, 101, 97, 100),

    # CLOSE STRICTLY ABOVE PROTECTED HIGH
    c("2026-04-07 00:40:00", 100, 106, 99, 104),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

invalidation = engine.last_invalidation()

check(
    invalidation is not None,
    "Bearish protected-level violation creates an invalidation event.",
)

check(
    invalidation.event == "STRUCTURE_INVALIDATION",
    "The event is classified as STRUCTURE_INVALIDATION.",
)

check(
    invalidation.direction == "BULLISH",
    "Bearish invalidation has BULLISH direction.",
)

check(
    invalidation.level == 103,
    "Invalidation occurs through the protected high at 103.",
)

check(
    invalidation.index == 8,
    "Invalidation occurs on the close-through candle.",
)

check(
    engine.bullish_invalidation(),
    "bullish_invalidation() correctly reports the invalidation.",
)


# ============================================================
# TEST 8
# INVALIDATION DOES NOT CREATE DUPLICATES
# ============================================================

section("TEST 8 — INVALIDATION DETERMINISM")

candles = [
    # 0
    c("2026-04-08 00:00:00", 100, 101, 99, 100),

    # 1 — INITIAL LOW
    c("2026-04-08 00:05:00", 100, 101, 97, 98),

    # 2 — INITIAL HIGH
    c("2026-04-08 00:10:00", 98, 106, 98, 104),

    # 3 — CONFIRM INITIAL HIGH
    c("2026-04-08 00:15:00", 104, 105, 101, 102),

    # 4 — BULLISH STRUCTURAL BREAK
    c("2026-04-08 00:20:00", 102, 109, 101, 107),

    # 5 — PULLBACK
    c("2026-04-08 00:25:00", 107, 108, 102, 103),

    # 6 — HIGHER-LOW CANDIDATE
    c("2026-04-08 00:30:00", 103, 106, 100, 105),

    # 7 — CONFIRM HIGHER LOW
    c("2026-04-08 00:35:00", 105, 107, 101, 104),

    # 8 — FIRST CLOSE THROUGH PROTECTED LOW
    c("2026-04-08 00:40:00", 104, 105, 96, 98),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

first = engine.last_invalidation()
second = engine.last_invalidation()

check(
    first == second,
    "Invalidation calculation is deterministic.",
)

check(
    first is not None,
    "An invalidation exists.",
)

check(
    first.event == "STRUCTURE_INVALIDATION",
    "Invalidation has the correct event type.",
)

check(
    first.direction == "BEARISH",
    "Bullish structure invalidates in the bearish direction.",
)

check(
    first.level == 100,
    "The protected low is the invalidation level.",
)

check(
    first.index == 8,
    "The first close-through candle remains authoritative.",
)


# ============================================================
# TEST 9
# SNAPSHOT CONSISTENCY
# ============================================================

section("TEST 9 — INVALIDATION SNAPSHOT")

snapshot = engine.snapshot()

print(snapshot)

check(
    "last_invalidation" in snapshot,
    "Snapshot exposes last_invalidation.",
)

check(
    snapshot["last_invalidation"] is not None,
    "Snapshot contains the invalidation event.",
)

check(
    snapshot["last_invalidation"]["event"]
    == "STRUCTURE_INVALIDATION",
    "Snapshot reports STRUCTURE_INVALIDATION.",
)

check(
    snapshot["last_invalidation"]["direction"]
    == "BEARISH",
    "Snapshot reports bearish invalidation direction.",
)

check(
    snapshot["last_invalidation"]["level"]
    == 100,
    "Snapshot preserves the historical protected-low invalidation level.",
)

check(
    snapshot["last_invalidation"]["index"]
    == 8,
    "Snapshot reports the first close-through candle as the invalidation candle.",
)

check(
    snapshot["last_invalidation"]["time"]
    == "2026-04-08 00:40:00",
    "Snapshot reports the correct invalidation candle time.",
)

check(
    snapshot["protected_low"] is None,
    "Current bearish structure has no bullish protected low.",
)

check(
    snapshot["protected_high"] is not None,
    "Current bearish structure exposes a protected high.",
)

check(
    snapshot["protected_high"]["price"] == 107,
    "Current bearish protected high is 107.",
)

print()
print("PASS: TEST 9 — INVALIDATION SNAPSHOT IS CONSISTENT.")


# ============================================================
# FINAL RESULT
# ============================================================

section("FINAL RESULT")

print("STRUCTURE INVALIDATION TESTS COMPLETED")
print()
print("Validated:")
print("  - no protected level")
print("  - bullish protected-low wick")
print("  - bullish exact protected-low close")
print("  - bullish close-through invalidation")
print("  - bearish protected-high wick")
print("  - bearish exact protected-high close")
print("  - bearish close-through invalidation")
print("  - invalidation determinism")
print("  - invalidation snapshot consistency")
print()
print("STRUCTURE INVALIDATION TEST: COMPLETE")