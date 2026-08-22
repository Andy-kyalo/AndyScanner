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
    print("BULLISH BOS     :", engine.bullish_bos())
    print("BEARISH BOS     :", engine.bearish_bos())
    print("BULLISH CHOCH   :", engine.bullish_choch())
    print("BEARISH CHOCH   :", engine.bearish_choch())
    print("PROTECTED HIGH  :", engine.protected_high())
    print("PROTECTED LOW   :", engine.protected_low())


# ============================================================
# TEST 1
# INITIAL BEARISH STRUCTURAL BREAK
# ============================================================

section("TEST 1 — INITIAL BEARISH STRUCTURAL BREAK")

candles = [
    c("2026-02-01 00:00:00", 100, 101, 99, 100),
    c("2026-02-01 00:05:00", 100, 105, 99, 104),

    # Initial swing HIGH
    c("2026-02-01 00:10:00", 104, 106, 98, 99),

    # Initial swing LOW candidate
    c("2026-02-01 00:15:00", 99, 102, 97, 101),

    # Confirms LOW at index 3
    c("2026-02-01 00:20:00", 101, 103, 100, 102),

    # Breaks confirmed LOW at 97
    c("2026-02-01 00:25:00", 102, 103, 95, 96),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

event = engine.current_event()

check(
    event is not None,
    "Initial bearish structural event exists.",
)

check(
    event.event == "STRUCTURE_BREAK",
    "Initial bearish event is STRUCTURE_BREAK.",
)

check(
    event.direction == "BEARISH",
    "Initial structural break direction is bearish.",
)

check(
    event.index == 5,
    "Bearish break occurs at index 5.",
)

check(
    event.level == 97,
    "Bearish break occurs through level 97.",
)

check(
    engine.structural_state() == "BEARISH",
    "Bearish structural state is established.",
)

check(
    engine.structure() == "BEARISH_STRUCTURE",
    "Structure is BEARISH_STRUCTURE.",
)


# ============================================================
# TEST 2
# BEARISH WICK MUST NOT CONFIRM
# ============================================================

section("TEST 2 — BEARISH WICK REJECTION")

candles = [
    c("2026-02-02 00:00:00", 100, 101, 99, 100),
    c("2026-02-02 00:05:00", 100, 105, 99, 104),

    # Initial HIGH
    c("2026-02-02 00:10:00", 104, 106, 98, 99),

    # Initial LOW
    c("2026-02-02 00:15:00", 99, 102, 97, 101),

    # Confirms LOW = 97
    c("2026-02-02 00:20:00", 101, 103, 100, 102),

    # Wick below 97, but CLOSE remains above 97
    c("2026-02-02 00:25:00", 102, 103, 95, 98),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

check(
    engine.current_event() is None,
    "Bearish wick below structural level does not confirm a break.",
)

check(
    engine.structural_state() == "UNDEFINED",
    "Wick-only move does not establish bearish structure.",
)


# ============================================================
# TEST 3
# BEARISH EXACT LEVEL MUST NOT CONFIRM
# ============================================================

section("TEST 3 — BEARISH EXACT LEVEL")

candles = [
    c("2026-02-03 00:00:00", 100, 101, 99, 100),
    c("2026-02-03 00:05:00", 100, 105, 99, 104),

    # Initial HIGH
    c("2026-02-03 00:10:00", 104, 106, 98, 99),

    # Initial LOW
    c("2026-02-03 00:15:00", 99, 102, 97, 101),

    # Confirms LOW = 97
    c("2026-02-03 00:20:00", 101, 103, 100, 102),

    # CLOSE exactly at 97
    c("2026-02-03 00:25:00", 102, 103, 95, 97),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

check(
    engine.current_event() is None,
    "Bearish close exactly at structural level does not confirm a break.",
)

check(
    engine.structural_state() == "UNDEFINED",
    "Exact-level close does not establish bearish structure.",
)


# ============================================================
# TEST 4
# INITIAL BEARISH BREAK IS NOT BOS OR CHOCH
# ============================================================

section("TEST 4 — INITIAL BEARISH BREAK CLASSIFICATION")

candles = [
    c("2026-02-04 00:00:00", 100, 101, 99, 100),
    c("2026-02-04 00:05:00", 100, 105, 99, 104),

    # Initial HIGH
    c("2026-02-04 00:10:00", 104, 106, 98, 99),

    # Initial LOW
    c("2026-02-04 00:15:00", 99, 102, 97, 101),

    # Confirms LOW = 97
    c("2026-02-04 00:20:00", 101, 103, 100, 102),

    # Initial bearish break
    c("2026-02-04 00:25:00", 102, 103, 95, 96),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

check(
    engine.current_event() is not None,
    "Initial bearish structural event exists.",
)

check(
    engine.current_event().event == "STRUCTURE_BREAK",
    "Initial bearish event remains STRUCTURE_BREAK.",
)

check(
    engine.bearish_bos() is False,
    "Initial bearish break is not BOS.",
)

check(
    engine.bearish_choch() is False,
    "Initial bearish break is not CHoCH.",
)

check(
    engine.bullish_bos() is False,
    "No bullish BOS exists.",
)

check(
    engine.bullish_choch() is False,
    "No bullish CHoCH exists.",
)


# ============================================================
# TEST 5
# BEARISH CONTINUATION / BOS
# ============================================================

section("TEST 5 — BEARISH BOS")

candles = [
    # --------------------------------------------------------
    # Initial structure
    # --------------------------------------------------------

    # 0
    c("2026-02-05 00:00:00", 100, 101, 99, 100),

    # 1 — INITIAL HIGH
    c("2026-02-05 00:05:00", 100, 106, 99, 104),

    # 2 — INITIAL LOW
    c("2026-02-05 00:10:00", 104, 105, 97, 99),

    # 3 — confirms LOW #1 at 97
    c("2026-02-05 00:15:00", 99, 102, 98, 101),

    # 4 — break below 97
    #     INITIAL BEARISH STRUCTURE
    c("2026-02-05 00:20:00", 101, 102, 95, 96),

    # --------------------------------------------------------
    # Lower-high formation
    # --------------------------------------------------------

    # 5 — rally
    c("2026-02-05 00:25:00", 96, 101, 95, 100),

    # 6 — LOWER HIGH candidate
    c("2026-02-05 00:30:00", 100, 103, 98, 99),

    # 7 — confirms LOWER HIGH at 103
    c("2026-02-05 00:35:00", 99, 100, 96, 97),

    # --------------------------------------------------------
    # New lower-low formation
    # --------------------------------------------------------

    # 8 — LOWER LOW candidate
    c("2026-02-05 00:40:00", 97, 99, 93, 94),

    # 9 — confirms LOWER LOW at 93
    c("2026-02-05 00:45:00", 94, 96, 94, 95),

    # --------------------------------------------------------
    # Break newly confirmed lower-low
    # --------------------------------------------------------

    # 10 — close strictly below 93
    c("2026-02-05 00:50:00", 95, 96, 91, 92),

    # 11 — continuation
    c("2026-02-05 00:55:00", 92, 94, 90, 91),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

events = engine.events()

print()
print("ALL EVENTS:")

for event in events:
    print(" ", event)

check(
    len(events) >= 2,
    "Initial bearish break and bearish continuation are detected.",
)

check(
    events[0].event == "STRUCTURE_BREAK",
    "First bearish event is STRUCTURE_BREAK.",
)

check(
    events[0].direction == "BEARISH",
    "First structural event is bearish.",
)

check(
    any(
        event.direction == "BEARISH"
        and event.event == "BOS"
        for event in events
    ),
    "A bearish BOS is detected after established bearish structure.",
)

check(
    engine.bearish_bos() is True,
    "bearish_bos() correctly reports a bearish BOS.",
)

last_bos = engine.last_bos()

check(
    last_bos is not None,
    "last_bos() returns the latest BOS event.",
)

check(
    last_bos.direction == "BEARISH",
    "Bearish BOS has BEARISH direction.",
)

check(
    last_bos.event == "BOS",
    "Bearish continuation is classified as BOS.",
)

check(
    last_bos.index == 10,
    "Bearish BOS occurs at index 10.",
)

check(
    last_bos.level == 93,
    "Bearish BOS breaks the 93 structural level.",
)


# ============================================================
# TEST 6
# BULLISH REVERSAL AFTER BEARISH STRUCTURE
# ============================================================

section("TEST 6 — BULLISH REVERSAL")

candles = [
    c("2026-02-06 00:00:00", 100, 101, 99, 100),

    # Initial HIGH
    c("2026-02-06 00:05:00", 100, 106, 99, 104),

    # Initial LOW
    c("2026-02-06 00:10:00", 104, 105, 97, 99),

    # Confirms LOW = 97
    c("2026-02-06 00:15:00", 99, 102, 98, 101),

    # Bearish break through 97
    c("2026-02-06 00:20:00", 101, 102, 94, 95),

    # Rally
    c("2026-02-06 00:25:00", 95, 103, 94, 102),

    # Pullback
    c("2026-02-06 00:30:00", 102, 104, 98, 99),

    # Higher close through 106
    c("2026-02-06 00:35:00", 99, 108, 98, 107),

    # Confirmation
    c("2026-02-06 00:40:00", 107, 109, 103, 108),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

events = engine.events()

print()
print("EVENT HISTORY:")

for event in events:
    print(" ", event)

check(
    len(events) >= 2,
    "Bearish structure followed by a later structural event.",
)

check(
    any(
        event.direction == "BEARISH"
        for event in events
    ),
    "Bearish structural event exists before reversal.",
)

check(
    any(
        event.direction == "BULLISH"
        for event in events
    ),
    "Bullish structural event exists after bearish structure.",
)


# ============================================================
# TEST 7
# BULLISH CHOCH
# ============================================================

section("TEST 7 — BULLISH CHOCH")

bullish_choch = engine.bullish_choch()

print("BULLISH CHOCH:", bullish_choch)

check(
    bullish_choch is True,
    "Bullish CHoCH exists after bearish structure.",
)

last_choch = engine.last_choch()

print("LAST CHOCH:", last_choch)

check(
    last_choch is not None,
    "last_choch() returns the latest CHoCH event.",
)

check(
    last_choch.event == "CHOCH",
    "Reversal event is classified as CHoCH.",
)

check(
    last_choch.direction == "BULLISH",
    "Bullish CHoCH has BULLISH direction.",
)

check(
    last_choch.index == 7,
    "Bullish CHoCH occurs at index 7.",
)

check(
    last_choch.level == 106,
    "Bullish CHoCH breaks the 106 structural high.",
)


# ============================================================
# TEST 8
# BEARISH CHOCH AFTER BULLISH STRUCTURE
# ============================================================

section("TEST 8 — BEARISH CHOCH")

candles = [
    # --------------------------------------------------------
    # Initial candle
    # --------------------------------------------------------

    c(
        "2026-02-08 00:00:00",
        100,
        101,
        99,
        100,
    ),

    # --------------------------------------------------------
    # Initial LOW
    # --------------------------------------------------------

    c(
        "2026-02-08 00:05:00",
        100,
        101,
        97,
        98,
    ),

    # --------------------------------------------------------
    # Initial HIGH
    # --------------------------------------------------------

    c(
        "2026-02-08 00:10:00",
        98,
        106,
        98,
        104,
    ),

    # --------------------------------------------------------
    # Confirms HIGH = 106
    # --------------------------------------------------------

    c(
        "2026-02-08 00:15:00",
        104,
        105,
        100,
        101,
    ),

    # --------------------------------------------------------
    # Bullish structural break
    # Close strictly above 106
    # --------------------------------------------------------

    c(
        "2026-02-08 00:20:00",
        101,
        109,
        100,
        107,
    ),

    # --------------------------------------------------------
    # Pullback
    # --------------------------------------------------------

    c(
        "2026-02-08 00:25:00",
        107,
        108,
        102,
        103,
    ),

    # --------------------------------------------------------
    # Rally / higher high
    # --------------------------------------------------------

    c(
        "2026-02-08 00:30:00",
        103,
        110,
        102,
        108,
    ),

    # --------------------------------------------------------
    # Bearish reversal
    # Close strictly below initial structural LOW = 97
    # --------------------------------------------------------

    c(
        "2026-02-08 00:35:00",
        108,
        109,
        95,
        96,
    ),

    # --------------------------------------------------------
    # Confirmation candle
    # --------------------------------------------------------

    c(
        "2026-02-08 00:40:00",
        96,
        99,
        93,
        94,
    ),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

bearish_choch = engine.bearish_choch()
last_choch = engine.last_choch()

print()
print("BEARISH CHOCH:", bearish_choch)
print("LAST CHOCH   :", last_choch)

check(
    bearish_choch is True,
    "Bearish CHoCH exists after bullish structure.",
)

check(
    last_choch is not None,
    "last_choch() returns the bearish reversal event.",
)

check(
    last_choch.event == "CHOCH",
    "Bearish reversal event is classified as CHoCH.",
)

check(
    last_choch.direction == "BEARISH",
    "Bearish CHoCH has BEARISH direction.",
)

check(
    last_choch.index == 7,
    "Bearish CHoCH occurs at index 7.",
)

check(
    last_choch.level == 97,
    "Bearish CHoCH breaks the 97 structural low.",
)


# ============================================================
# TEST 9
# PROTECTED LEVELS
# ============================================================

section("TEST 9 — PROTECTED LEVELS")

protected_high = engine.protected_high()
protected_low = engine.protected_low()

print("PROTECTED HIGH:", protected_high)
print("PROTECTED LOW :", protected_low)

if protected_high is not None:
    check(
        protected_high.kind == "HIGH",
        "Protected high is a HIGH structure point.",
    )

if protected_low is not None:
    check(
        protected_low.kind == "LOW",
        "Protected low is a LOW structure point.",
    )

check(
    protected_high is None
    or protected_high.kind == "HIGH",
    "Protected high is structurally valid.",
)

check(
    protected_low is None
    or protected_low.kind == "LOW",
    "Protected low is structurally valid.",
)


# ============================================================
# TEST 10
# NO DUPLICATE BEARISH BREAK
# ============================================================

section("TEST 10 — NO DUPLICATE BEARISH BREAK")

candles = [
    c("2026-02-09 00:00:00", 100, 101, 99, 100),

    # HIGH
    c("2026-02-09 00:05:00", 100, 106, 99, 104),

    # LOW
    c("2026-02-09 00:10:00", 104, 105, 97, 99),

    # Confirms LOW
    c("2026-02-09 00:15:00", 99, 102, 98, 101),

    # First bearish break
    c("2026-02-09 00:20:00", 101, 102, 94, 95),

    # Remains below same level
    c("2026-02-09 00:25:00", 95, 98, 92, 94),

    c("2026-02-09 00:30:00", 94, 97, 91, 93),
]

engine = MarketStructureEngine(
    candles,
    swing_strength=1,
)

show_engine(engine)

bearish_events = [
    event
    for event in engine.events()
    if event.direction == "BEARISH"
]

check(
    len(bearish_events) == 1,
    "The same bearish structural level produces only one event.",
)

check(
    bearish_events[0].event == "STRUCTURE_BREAK",
    "The unique bearish event is the initial structural break.",
)

check(
    bearish_events[0].direction == "BEARISH",
    "The unique event has bearish direction.",
)

check(
    bearish_events[0].level == 97,
    "The duplicate-prevention level is 97.",
)


# ============================================================
# TEST 11
# EVENT ORDER
# ============================================================

section("TEST 11 — EVENT ORDER")

events = engine.events()

print("EVENT COUNT:", len(events))

for event in events:
    print(" ", event)

check(
    events == sorted(
        events,
        key=lambda event: event.index,
    ),
    "Structure events are chronologically ordered.",
)

for first, second in zip(events, events[1:]):
    check(
        first.index < second.index,
        "Structure events remain strictly chronological.",
    )


# ============================================================
# TEST 12
# SNAPSHOT CONSISTENCY
# ============================================================

section("TEST 12 — SNAPSHOT CONSISTENCY")

snapshot = engine.snapshot()

print(snapshot)

required_keys = {
    "trend",
    "structural_state",
    "structure",
    "current_event",
    "bullish_bos",
    "bearish_bos",
    "bullish_choch",
    "bearish_choch",
    "swing_high_count",
    "swing_low_count",
    "latest_high",
    "latest_low",
    "protected_high",
    "protected_low",
    "last_structure_break",
    "last_bos",
    "last_choch",
    "event_count",
}

for key in required_keys:
    check(
        key in snapshot,
        f"Snapshot contains '{key}'.",
    )

events = engine.events()

check(
    snapshot["event_count"] == len(events),
    "Snapshot event count matches event history.",
)

check(
    snapshot["swing_high_count"] == engine.swing_high_count(),
    "Snapshot high count matches engine.",
)

check(
    snapshot["swing_low_count"] == engine.swing_low_count(),
    "Snapshot low count matches engine.",
)

check(
    snapshot["bearish_choch"] is False,
    "Snapshot correctly reports no CHoCH in duplicate-break fixture.",
)

check(
    snapshot["last_choch"] is None,
    "Snapshot correctly reports no CHoCH event in duplicate-break fixture.",
)

latest_high = engine.latest_swing_high()
latest_low = engine.latest_swing_low()

if latest_high is None:
    check(
        snapshot["latest_high"] is None,
        "Snapshot latest high is consistently None.",
    )
else:
    check(
        snapshot["latest_high"]["index"] == latest_high.index,
        "Snapshot latest high index matches engine.",
    )

    check(
        snapshot["latest_high"]["price"] == latest_high.price,
        "Snapshot latest high price matches engine.",
    )

if latest_low is None:
    check(
        snapshot["latest_low"] is None,
        "Snapshot latest low is consistently None.",
    )
else:
    check(
        snapshot["latest_low"]["index"] == latest_low.index,
        "Snapshot latest low index matches engine.",
    )

    check(
        snapshot["latest_low"]["price"] == latest_low.price,
        "Snapshot latest low price matches engine.",
    )


# ============================================================
# TEST 13
# DETERMINISM
# ============================================================

section("TEST 13 — DETERMINISM")

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
# FINAL RESULT
# ============================================================

section("FINAL RESULT")

print("REVERSAL MARKET STRUCTURE TESTS COMPLETED")
print()
print("Validated:")
print("  - initial bearish structural break")
print("  - bearish close-through semantics")
print("  - bearish wick rejection")
print("  - bearish exact-level rejection")
print("  - initial-break classification")
print("  - bearish continuation")
print("  - bearish BOS")
print("  - bullish reversal")
print("  - bullish CHoCH")
print("  - bearish reversal")
print("  - bearish CHoCH")
print("  - protected levels")
print("  - duplicate-break prevention")
print("  - chronological event ordering")
print("  - snapshot consistency")
print("  - deterministic calculations")
print()
print("REVERSAL MARKET STRUCTURE TEST: COMPLETE")