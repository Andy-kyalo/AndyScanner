class Signal:

    def __init__(self, market, timeframe, direction, confidence):
        self.market = market
        self.timeframe = timeframe
        self.direction = direction
        self.confidence = confidence

    def show(self):
        print("========== Trading Signal ==========")
        print(f"Market      : {self.market}")
        print(f"Timeframe   : {self.timeframe}")
        print(f"Direction   : {self.direction}")
        print(f"Confidence  : {self.confidence}%")
        print("====================================")