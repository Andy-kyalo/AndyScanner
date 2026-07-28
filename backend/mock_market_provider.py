"""
mock_market_provider.py

Mock market provider used for testing Andy Scanner
without connecting to a real broker.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.market_provider import MarketProvider
from backend.market_data import MarketData


class MockMarketProvider(MarketProvider):
    """
    Simulated market data provider.
    """

    def __init__(self, symbol="US30", timeframe="M5"):

        super().__init__(symbol, timeframe)

        self.connected = False

    # ==========================================
    # Connection
    # ==========================================

    def connect(self):

        self.connected = True

    def disconnect(self):

        self.connected = False

    def is_connected(self):

        return self.connected

    # ==========================================
    # Latest Candle
    # ==========================================

    def get_latest_candle(self):

        return MarketData(
            symbol=self.symbol,
            timeframe=self.timeframe,
            time="22:15",
            open=45135.80,
            high=45200.00,
            low=45091.00,
            close=45180.00,
            volume=1250,
        )

    # ==========================================
    # Historical Candles
    # ==========================================

    def get_candles(self, limit=100):

        candles = [

            MarketData(
                self.symbol,
                self.timeframe,
                "22:00",
                45020.50,
                45110.75,
                44980.25,
                45110.75,
                1100,
            ),

            MarketData(
                self.symbol,
                self.timeframe,
                "22:05",
                45095.30,
                45150.00,
                45070.00,
                45130.20,
                950,
            ),

            MarketData(
                self.symbol,
                self.timeframe,
                "22:10",
                45130.20,
                45160.50,
                45120.00,
                45130.00,
                870,
            ),

            MarketData(
                self.symbol,
                self.timeframe,
                "22:15",
                45135.80,
                45200.00,
                45091.00,
                45180.00,
                1250,
            ),
        ]

        return candles[:limit]