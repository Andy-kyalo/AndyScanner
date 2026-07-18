
import time


from backend.loader import Loader
from backend.analyzer import Analyzer
from backend.logger import Logger


class ScannerEngine:

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.logger = Logger()

    def run(self):

        try:
            start_time = time.time()
            self.logger.session_log("===== SESSION STARTED =====")

            self.logger.info("Scanner", "Starting market scan.")

            loader = Loader(self.csv_file)
            candles = loader.load()
            self.logger.session_log("Market: US30")
            self.logger.session_log("Timeframe: M5")
            self.logger.session_log(f"Candles Loaded: {len(candles)}")

            analyzer = Analyzer(candles)
            signal = analyzer.generate_signal()
            self.logger.session_log(
                f"Signal Direction: {signal.direction}"
)

            self.logger.session_log(
                f"Signal Confidence: {signal.confidence}%"
)

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
            end_time = time.time()
            duration = round(end_time - start_time, 4)

            self.logger.session_log(
                f"Scan Duration: {duration} seconds"
             
)        
            self.logger.session_log("Status: SUCCESS")  
            
          
            self.logger.session_log("===== SESSION COMPLETED =====")

            return {
                "candles": candles,
                "analyzer": analyzer,
                "signal": signal,
            }

        except Exception as error:

            self.logger.error_log(
                f"ScannerEngine failed: {error}"
            )
            self.logger.session_log("Status: FAILED")
            self.logger.session_log("===== SESSION TERMINATED =====")

            raise