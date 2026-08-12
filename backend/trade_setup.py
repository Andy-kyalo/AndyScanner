"""
trade_setup.py

Structured trade setup produced after signal generation.

Author: Andrew Kyalo
Project: Andy Scanner
"""


class TradeSetup:
    """
    Represents a potential trade setup.

    This object describes the trade structure without
    deciding whether the setup passes final risk validation.
    """

    def __init__(
        self,
        market,
        timeframe,
        direction,
        entry=None,
        stop_loss=None,
        take_profit=None,
        risk_reward=None,
        valid=False,
    ):

        self.market = market
        self.timeframe = timeframe

        self.direction = direction

        self.entry = entry
        self.stop_loss = stop_loss
        self.take_profit = take_profit

        self.risk_reward = risk_reward

        self.valid = valid

    def summary(self):

        return {
            "market": self.market,
            "timeframe": self.timeframe,
            "direction": self.direction,
            "entry": self.entry,
            "stop_loss": self.stop_loss,
            "take_profit": self.take_profit,
            "risk_reward": self.risk_reward,
            "valid": self.valid,
        }

    def __repr__(self):

        return (
            f"TradeSetup("
            f"market={self.market}, "
            f"timeframe={self.timeframe}, "
            f"direction={self.direction}, "
            f"entry={self.entry}, "
            f"stop_loss={self.stop_loss}, "
            f"take_profit={self.take_profit}, "
            f"risk_reward={self.risk_reward}, "
            f"valid={self.valid})"
        )
