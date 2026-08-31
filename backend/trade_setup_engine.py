"""
trade_setup_engine.py

Deterministic Trade Setup Engine for Andy Scanner.

Converts a completed market analysis and trading signal
into a structured trade setup.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.trade_setup import TradeSetup


class TradeSetupEngine:
    """
    Generates deterministic trade setups from:

        - validated candles
        - AnalysisResult
        - Signal

    The engine never invents missing market levels.
    If a required structural level is unavailable,
    the resulting setup is invalid.
    """

    def __init__(self, analysis, signal, candles):

        self.analysis = analysis
        self.signal = signal
        self.candles = candles

    # ==================================================
    # Generate
    # ==================================================

    def generate(self):
        """
        Generate a complete trade setup.
        """

        direction = self.signal.direction

        if direction == "WAIT":
            return self._invalid_setup()

        if direction in ("BUY", "STRONG BUY"):
            return self._generate_buy_setup()

        if direction in ("SELL", "STRONG SELL"):
            return self._generate_sell_setup()

        return self._invalid_setup()

    # ==================================================
    # BUY SETUP
    # ==================================================

    def _generate_buy_setup(self):

        entry = self._find_entry()

        stop_loss = self._find_buy_stop_loss()

        take_profit = self._find_buy_take_profit(
            entry
        )

        return self._build_setup(
            direction=self.signal.direction,
            entry=entry,
            stop_loss=stop_loss,
            take_profit=take_profit,
        )

    # ==================================================
    # SELL SETUP
    # ==================================================

    def _generate_sell_setup(self):

        entry = self._find_entry()

        stop_loss = self._find_sell_stop_loss()

        take_profit = self._find_sell_take_profit(
            entry
        )

        return self._build_setup(
            direction=self.signal.direction,
            entry=entry,
            stop_loss=stop_loss,
            take_profit=take_profit,
        )

    # ==================================================
    # ENTRY
    # ==================================================

    def _find_entry(self):

        if not self.candles:
            return None

        return self.candles[-1].close

    # ==================================================
    # BUY STOP LOSS
    # ==================================================

    def _find_buy_stop_loss(self):

        order_block = (
            self.analysis.bullish_order_block
        )

        if order_block is None:
            return None

        return order_block.low

    # ==================================================
    # SELL STOP LOSS
    # ==================================================

    def _find_sell_stop_loss(self):

        order_block = (
            self.analysis.bearish_order_block
        )

        if order_block is None:
            return None

        return order_block.high

    # ==================================================
    # BUY TAKE PROFIT
    # ==================================================

    def _find_buy_take_profit(self, entry):

        if entry is None:
            return None

        candidates = []

        for candle in (
            self.analysis.buy_side_liquidity
        ):

            level = candle.high

            if level > entry:
                candidates.append(level)

        if not candidates:
            return None

        return min(candidates)

    # ==================================================
    # SELL TAKE PROFIT
    # ==================================================

    def _find_sell_take_profit(self, entry):

        if entry is None:
            return None

        candidates = []

        for candle in (
            self.analysis.sell_side_liquidity
        ):

            level = candle.low

            if level < entry:
                candidates.append(level)

        if not candidates:
            return None

        return max(candidates)

    # ==================================================
    # BUILD SETUP
    # ==================================================

    def _build_setup(
        self,
        direction,
        entry,
        stop_loss,
        take_profit,
    ):

        valid = self._validate_levels(
            direction,
            entry,
            stop_loss,
            take_profit,
        )

        risk_reward = None

        if valid:

            risk = abs(
                entry - stop_loss
            )

            reward = abs(
                take_profit - entry
            )

            if risk > 0:

                risk_reward = round(
                    reward / risk,
                    2,
                )

            else:

                valid = False

        return TradeSetup(
            market=self.analysis.market,
            timeframe=self.analysis.timeframe,
            direction=direction,
            entry=entry,
            stop_loss=stop_loss,
            take_profit=take_profit,
            risk_reward=risk_reward,
            valid=valid,
        )

    # ==================================================
    # VALIDATION
    # ==================================================

    def _validate_levels(
        self,
        direction,
        entry,
        stop_loss,
        take_profit,
    ):

        if entry is None:
            return False

        if stop_loss is None:
            return False

        if take_profit is None:
            return False

        if direction in ("BUY", "STRONG BUY"):

            return (
                stop_loss < entry
                and entry < take_profit
            )

        if direction in ("SELL", "STRONG SELL"):

            return (
                take_profit < entry
                and entry < stop_loss
            )

        return False

    # ==================================================
    # INVALID SETUP
    # ==================================================

    def _invalid_setup(self):

        return TradeSetup(
            market=self.analysis.market,
            timeframe=self.analysis.timeframe,
            direction=self.signal.direction,
            entry=None,
            stop_loss=None,
            take_profit=None,
            risk_reward=None,
            valid=False,
        )
