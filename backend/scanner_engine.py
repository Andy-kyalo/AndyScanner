from backend.loader import Loader
from backend.analyzer import Analyzer


class ScannerEngine:

    def __init__(self, csv_file):
        self.csv_file = csv_file

    def run(self):

        loader = Loader(self.csv_file)
        candles = loader.load()

        analyzer = Analyzer(candles)

        signal = analyzer.generate_signal()

        return {
            "candles": candles,
            "analyzer": analyzer,
            "signal": signal,
        }