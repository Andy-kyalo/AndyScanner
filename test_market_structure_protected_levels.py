from backend.candle import Candle
from backend.market_structure_engine import MarketStructureEngine


# ============================================================
# HELPERS
# ============================================================

def c(time, o, h, l, cl):
    """
    Create a validated Candle.

    OHLC requirements:

        low <= open
        low <= close
        high >= open
        high >= close
    """
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
# TEST 1
# INSUFFICIENT BULLISH STRUCTURE
# ============================================================

section("TEST 1 — INSUFFICIENT BULLISH STRUCTURE")

candles = [
    # 0
    c("2026-03-01 00:00:00", 100, 101, 99, 100),

    # 1 — INITIAL LOW
    c("2026-03-01 00:05:00", 100, 101, 97, 98),

    # 2 — INITIAL HIGH
    #
    # IMPORTANT:
    # low = 99
    # open = 99
    #
    # This satisfies the Candle OHLC invariant and
    # keeps index 1 as the confirmed swing low.
    c("2026-03-01 00:10:00", 99, 106, 99, 104),

    # 3 — CONFIRMATION
    c("2026-03-01 00:15:00", 104, 105, 100, 102),

    # 4 — BULLISH STRUCTURAL BREAK
    c("2026-03-01 00:20:00", 102, 109, 101, 107),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

check(
    engine.structural_state() == "BULLISH",
    "Bullish structural state is established.",
)

check(
    engine.protected_low() is None,
    "Protected low is not created from insufficient structural history.",
)

check(
    engine.protected_high() is None,
    "Protected high is not created from insufficient structural history.",
)


# ============================================================
# TEST 2
# BULLISH STRUCTURE WITH PROTECTED LOW
# ============================================================

section("TEST 2 — BULLISH PROTECTED LOW")

candles = [
    # 0
    c("2026-03-02 00:00:00", 100, 101, 99, 100),

    # 1 — INITIAL LOW
    c("2026-03-02 00:05:00", 100, 101, 97, 98),

    # 2 — INITIAL HIGH
    #
    # Valid OHLC:
    # open = 99
    # high = 106
    # low = 99
    # close = 104
    #
    # low is higher than the low at index 1,
    # allowing index 1 to remain the swing low.
    c("2026-03-02 00:10:00", 99, 106, 99, 104),

    # 3 — CONFIRMS HIGH
    c("2026-03-02 00:15:00", 104, 105, 100, 102),

    # 4 — BULLISH STRUCTURAL BREAK
    c("2026-03-02 00:20:00", 102, 109, 101, 107),

    # 5 — PULLBACK
    c("2026-03-02 00:25:00", 107, 108, 103, 104),

    # 6 — NEW HIGH CANDIDATE
    c("2026-03-02 00:30:00", 104, 110, 102, 108),

    # 7 — CONFIRMS HIGH
    c("2026-03-02 00:35:00", 108, 109, 104, 107),

    # 8 — NEW HIGHER-LOW CANDIDATE
    c("2026-03-02 00:40:00", 107, 108, 103, 104),

    # 9 — CONFIRMS HIGHER LOW
    c("2026-03-02 00:45:00", 104, 106, 104, 105),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

protected_low = engine.protected_low()

check(
    protected_low is not None,
    "Bullish structure exposes a protected low when sufficient structure exists.",
)

check(
    protected_low.kind == "LOW",
    "Bullish protected level is a LOW.",
)

check(
    protected_low.price == 103,
    "Bullish protected low is the structurally significant higher low at 103."
)

check(
    protected_low.index == 8,
    "Bullish protected low comes from confirmed swing index 8.",
)

check(
    protected_low.label == "HL",
    "Bullish protected low is classified as a higher low.",
)


# ============================================================
# TEST 3
# BULLISH WICK BELOW PROTECTED LOW
# ============================================================

section("TEST 3 — BULLISH PROTECTED LOW WICK")

candles = [
    # 0
    c("2026-03-03 00:00:00", 100, 101, 99, 100),

    # 1 — INITIAL LOW
    c("2026-03-03 00:05:00", 100, 101, 97, 98),

    # 2 — INITIAL HIGH
    c("2026-03-03 00:10:00", 99, 106, 99, 104),

    # 3 — CONFIRMS HIGH
    c("2026-03-03 00:15:00", 104, 105, 100, 102),

    # 4 — BULLISH STRUCTURAL BREAK
    c("2026-03-03 00:20:00", 102, 109, 101, 107),

    # 5 — PULLBACK
    c("2026-03-03 00:25:00", 107, 108, 103, 104),

    # 6 — PROTECTED LOW CANDIDATE
    c("2026-03-03 00:30:00", 104, 106, 100, 103),

    # 7 — CONFIRMS LOW
    c("2026-03-03 00:35:00", 103, 105, 102, 105),

    # 8 — WICK BELOW PROTECTED LOW = 100
    #
    # low = 98
    # close = 102
    #
    # The wick violates the level intrabar,
    # but the close remains above it.
    c("2026-03-03 00:40:00", 105, 107, 98, 102),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

protected_low = engine.protected_low()

check(
    protected_low is not None,
    "A protected low exists before the wick test.",
)

check(
    protected_low.price == 100,
    "The protected low is 100 before the wick test.",
)

check(
    engine.structural_state() == "BULLISH",
    "Bullish structure remains valid after a protected-low wick.",
)

check(
    engine.current_event() is not None,
    "Structural history remains available after the wick.",
)

check(
    engine.current_event().direction == "BULLISH",
    "Wick below protected low does not reverse structural direction.",
)


# ============================================================
# TEST 4
# BULLISH EXACT PROTECTED LEVEL
# ============================================================

section("TEST 4 — BULLISH PROTECTED LOW EXACT CLOSE")

candles = [
    # 0
    c("2026-03-04 00:00:00", 100, 101, 99, 100),

    # 1 — INITIAL LOW
    c("2026-03-04 00:05:00", 100, 101, 97, 98),

    # 2 — INITIAL HIGH
    c("2026-03-04 00:10:00", 99, 106, 99, 104),

    # 3 — CONFIRMS HIGH
    c("2026-03-04 00:15:00", 104, 105, 100, 102),

    # 4 — BULLISH STRUCTURAL BREAK
    c("2026-03-04 00:20:00", 102, 109, 101, 107),

    # Pullback / protected-low candidate
    c("2026-03-04 00:25:00", 107, 108, 100, 103),

    # Confirmation
    c("2026-03-04 00:30:00", 103, 106, 102, 105),

    # CLOSE exactly at protected low 100
    c("2026-03-04 00:35:00", 105, 106, 99, 100),

    # 8 — CLOSE EXACTLY AT PROTECTED LOW = 100
    #
    # low = 99
    # close = 100
    c("2026-03-04 00:40:00", 105, 106, 99, 100),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

protected_low = engine.protected_low()

check(
    protected_low is not None,
    "A protected low exists before the exact-level test.",
)

check(
    protected_low.price == 100,
    "The protected low is 100 before the exact-level test.",
)

check(
    engine.structural_state() == "BULLISH",
    "Close exactly at protected low does not invalidate bullish structure.",
)

check(
    engine.bullish_choch() is False,
    "Exact protected-low close does not create a bearish CHoCH.",
)


# ============================================================
# TEST 5
# BEARISH STRUCTURE WITH PROTECTED HIGH
# ============================================================

section("TEST 5 — BEARISH PROTECTED HIGH")

candles = [
    # 0
    c("2026-03-05 00:00:00", 100, 101, 99, 100),

    # 1 — INITIAL HIGH
    c("2026-03-05 00:05:00", 100, 106, 99, 104),

    # 2 — INITIAL LOW
    c("2026-03-05 00:10:00", 104, 105, 97, 99),

    # 3 — CONFIRMS LOW
    c("2026-03-05 00:15:00", 99, 102, 98, 101),

    # 4 — BEARISH STRUCTURAL BREAK
    c("2026-03-05 00:20:00", 101, 102, 95, 96),

    # 5 — RALLY
    c("2026-03-05 00:25:00", 96, 101, 95, 100),

    # 6 — LOWER HIGH CANDIDATE
    c("2026-03-05 00:30:00", 100, 103, 98, 99),

    # 7 — CONFIRMS LOWER HIGH
    c("2026-03-05 00:35:00", 99, 100, 96, 97),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

protected_high = engine.protected_high()

check(
    protected_high is not None,
    "Bearish structure exposes a protected high when sufficient structure exists.",
)

check(
    protected_high.kind == "HIGH",
    "Bearish protected level is a HIGH.",
)

check(
    protected_high.price == 103,
    "Bearish protected high is the structurally significant high at 103.",
)

check(
    protected_high.index == 6,
    "Bearish protected high comes from confirmed swing index 6.",
)

check(
    protected_high.label == "LH",
    "Bearish protected high is classified as a lower high.",
)


# ============================================================
# TEST 6
# BEARISH WICK ABOVE PROTECTED HIGH
# ============================================================

section("TEST 6 — BEARISH PROTECTED HIGH WICK")

candles = [
    # 0
    c("2026-03-06 00:00:00", 100, 101, 99, 100),

    # 1 — INITIAL HIGH
    c("2026-03-06 00:05:00", 100, 106, 99, 104),

    # 2 — INITIAL LOW
    c("2026-03-06 00:10:00", 104, 105, 97, 99),

    # 3 — CONFIRMS LOW
    c("2026-03-06 00:15:00", 99, 102, 98, 101),

    # 4 — BEARISH STRUCTURAL BREAK
    c("2026-03-06 00:20:00", 101, 102, 95, 96),

    # 5 — RALLY
    c("2026-03-06 00:25:00", 96, 101, 95, 100),

    # 6 — LOWER HIGH CANDIDATE
    c("2026-03-06 00:30:00", 100, 103, 98, 99),

    # 7 — CONFIRMS LOWER HIGH
    c("2026-03-06 00:35:00", 99, 100, 96, 97),

    # 8 — WICK ABOVE PROTECTED HIGH = 103
    c("2026-03-06 00:40:00", 97, 105, 95, 101),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

protected_high = engine.protected_high()

check(
    protected_high is not None,
    "A protected high exists before the wick test.",
)

check(
    protected_high.price == 103,
    "The protected high is 103 before the wick test.",
)

check(
    engine.structural_state() == "BEARISH",
    "Bearish structure remains valid after a protected-high wick.",
)

check(
    engine.current_event() is not None,
    "Structural history remains available after the wick.",
)

check(
    engine.current_event().direction == "BEARISH",
    "Wick above protected high does not reverse structural direction.",
)


# ============================================================
# TEST 7
# BEARISH EXACT PROTECTED LEVEL
# ============================================================

section("TEST 7 — BEARISH PROTECTED HIGH EXACT CLOSE")

candles = [
    # 0
    c("2026-03-07 00:00:00", 100, 101, 99, 100),

    # 1 — INITIAL HIGH
    c("2026-03-07 00:05:00", 100, 106, 99, 104),

    # 2 — INITIAL LOW
    c("2026-03-07 00:10:00", 104, 105, 97, 99),

    # 3 — CONFIRMS LOW
    c("2026-03-07 00:15:00", 99, 102, 98, 101),

    # 4 — BEARISH STRUCTURAL BREAK
    c("2026-03-07 00:20:00", 101, 102, 95, 96),

    # 5 — RALLY
    c("2026-03-07 00:25:00", 96, 101, 95, 100),

    # 6 — LOWER HIGH CANDIDATE
    c("2026-03-07 00:30:00", 100, 103, 98, 99),

    # 7 — CONFIRMS LOWER HIGH
    c("2026-03-07 00:35:00", 99, 100, 96, 97),

    # 8 — CLOSE EXACTLY AT PROTECTED HIGH = 103
    c("2026-03-07 00:40:00", 103, 104, 96, 103),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

protected_high = engine.protected_high()

check(
    protected_high is not None,
    "A protected high exists before the exact-level test.",
)

check(
    protected_high.price == 103,
    "The protected high is 103 before the exact-level test.",
)

check(
    engine.structural_state() == "BEARISH",
    "Close exactly at protected high does not invalidate bearish structure.",
)

check(
    engine.bearish_choch() is False,
    "Exact protected-high close does not create a bullish CHoCH.",
)


# ============================================================
# TEST 8
# PROTECTED LEVEL API CONSISTENCY
# ============================================================

section("TEST 8 — PROTECTED LEVEL API CONSISTENCY")

bullish_engine = MarketStructureEngine(
    [
        # 0
        c("2026-03-08 00:00:00", 100, 101, 99, 100),

        # 1 — INITIAL LOW
        c("2026-03-08 00:05:00", 100, 101, 97, 98),

        # 2 — INITIAL HIGH
        c("2026-03-08 00:10:00", 99, 106, 99, 104),

        # 3 — CONFIRMS HIGH
        c("2026-03-08 00:15:00", 104, 105, 100, 102),

        # 4 — BULLISH BREAK
        c("2026-03-08 00:20:00", 102, 109, 101, 107),

        # 5 — PULLBACK
        c("2026-03-08 00:25:00", 107, 108, 103, 104),

        # 6 — PROTECTED LOW CANDIDATE
        c("2026-03-08 00:30:00", 104, 106, 100, 103),

        # 7 — CONFIRMS LOW
        c("2026-03-08 00:35:00", 103, 105, 101, 105),
    ],
    swing_strength=1,
)

bearish_engine = MarketStructureEngine(
    [
        # 0
        c("2026-03-09 00:00:00", 100, 101, 99, 100),

        # 1 — INITIAL HIGH
        c("2026-03-09 00:05:00", 100, 106, 99, 104),

        # 2 — INITIAL LOW
        c("2026-03-09 00:10:00", 104, 105, 97, 99),

        # 3 — CONFIRMS LOW
        c("2026-03-09 00:15:00", 99, 102, 98, 101),

        # 4 — BEARISH BREAK
        c("2026-03-09 00:20:00", 101, 102, 95, 96),

        # 5 — RALLY
        c("2026-03-09 00:25:00", 96, 101, 95, 100),

        # 6 — PROTECTED HIGH CANDIDATE
        c("2026-03-09 00:30:00", 100, 103, 98, 99),

        # 7 — CONFIRMS HIGH
        c("2026-03-09 00:35:00", 99, 100, 96, 97),
    ],
    swing_strength=1,
)

bullish_snapshot = bullish_engine.snapshot()
bearish_snapshot = bearish_engine.snapshot()

print("BULLISH SNAPSHOT:")
print(bullish_snapshot)

print()
print("BEARISH SNAPSHOT:")
print(bearish_snapshot)

check(
    "protected_low" in bullish_snapshot,
    "Bullish snapshot exposes protected_low.",
)

check(
    "protected_high" in bullish_snapshot,
    "Bullish snapshot exposes protected_high.",
)

check(
    "protected_low" in bearish_snapshot,
    "Bearish snapshot exposes protected_low.",
)

check(
    "protected_high" in bearish_snapshot,
    "Bearish snapshot exposes protected_high.",
)

check(
    bullish_snapshot["protected_low"] is not None,
    "Bullish snapshot contains a protected low.",
)

check(
    bullish_snapshot["protected_low"]["price"] == 100,
    "Bullish snapshot reports protected low price 100.",
)

check(
    bearish_snapshot["protected_high"] is not None,
    "Bearish snapshot contains a protected high.",
)

check(
    bearish_snapshot["protected_high"]["price"] == 103,
    "Bearish snapshot reports protected high price 103.",
)


# ============================================================
# TEST 9
# PROTECTED LEVEL STRUCTURAL CONSISTENCY
# ============================================================

section("TEST 9 — PROTECTED LEVEL STRUCTURAL CONSISTENCY")

bullish_protected = bullish_engine.protected_low()
bearish_protected = bearish_engine.protected_high()

check(
    bullish_engine.structural_state() == "BULLISH",
    "Bullish fixture has bullish structural state.",
)

check(
    bullish_protected is not None,
    "Bullish fixture has a protected low.",
)

check(
    bullish_protected.kind == "LOW",
    "Bullish protected level is structurally a LOW.",
)

check(
    bullish_protected.label == "HL",
    "Bullish protected low is classified as HL.",
)

check(
    bearish_engine.structural_state() == "BEARISH",
    "Bearish fixture has bearish structural state.",
)

check(
    bearish_protected is not None,
    "Bearish fixture has a protected high.",
)

check(
    bearish_protected.kind == "HIGH",
    "Bearish protected level is structurally a HIGH.",
)

check(
    bearish_protected.label == "LH",
    "Bearish protected high is classified as LH.",
)


# ============================================================
# TEST 10
# DETERMINISM
# ============================================================

section("TEST 10 — DETERMINISM")

snapshot_1 = bullish_engine.snapshot()
snapshot_2 = bullish_engine.snapshot()

check(
    snapshot_1 == snapshot_2,
    "Protected-level snapshots remain deterministic.",
)

check(
    bullish_engine.protected_low()
    == bullish_engine.protected_low(),
    "Protected low calculation is deterministic.",
)

check(
    bearish_engine.protected_high()
    == bearish_engine.protected_high(),
    "Protected high calculation is deterministic.",
)

check(
    bullish_engine.events() == bullish_engine.events(),
    "Bullish event history remains deterministic.",
)

check(
    bearish_engine.events() == bearish_engine.events(),
    "Bearish event history remains deterministic.",
)


# ============================================================
# FINAL RESULT
# ============================================================

section("FINAL RESULT")

print("PROTECTED LEVEL TESTS COMPLETED")
print()
print("Validated:")
print("  - insufficient protected-level history")
print("  - bullish protected low")
print("  - bullish protected-low wick")
print("  - bullish protected-low exact close")
print("  - bearish protected high")
print("  - bearish protected-high wick")
print("  - bearish protected-high exact close")
print("  - protected-level snapshot API")
print("  - protected-level structural consistency")
print("  - deterministic protected levels")
print("  - deterministic event history")
print()
print("PROTECTED LEVEL TEST: COMPLETE")