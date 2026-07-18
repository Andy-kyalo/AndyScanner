from backend.loader import Loader
from backend.analyzer import Analyzer
from backend.logger import Logger

class ScannerEngine:

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.logger = Logger()
    def run(self):

        self.logger.info("Scanner", "Starting market scan.")

        loader = Loader(self.csv_file)
        candles = loader.load()

        analyzer = Analyzer(candles)
        signal = analyzer.generate_signal()
        self.logger.signal_log(
        f"Market={signal.market} | "
        f"Timeframe={signal.timeframe} | "
        f"Direction={signal.direction} | "
        f"Confidence={signal.confidence}%"
)

        self.logger.info(
            "Scanner",
            f"Scan completed successfully. Loaded {len(candles)} candles."
    )

        return {
            "candles": candles,
            "analyzer": analyzer,
            "signal": signal,
    }