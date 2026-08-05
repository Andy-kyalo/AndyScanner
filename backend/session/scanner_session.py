"""
Andy Scanner
Professional Scanner Session Manager
Version 5.3
"""

from datetime import datetime
import uuid


class ScannerSession:
    """
    Stores information about a scanner execution session.
    """

    def __init__(self, market: str, timeframe: str):
        self.session_id = str(uuid.uuid4())[:8].upper()

        self.market = market
        self.timeframe = timeframe

        self.started_at = datetime.now()
        self.last_scan = None

        self.execution_time = 0.0

        self.provider = "Unknown"

        self.analysis_status = "Not Started"

        self.candles_processed = 0

        self.trend = "UNKNOWN"
        self.signal = "WAIT"
        self.confidence = 0

    def update_scan(
        self,
        trend,
        signal,
        confidence,
        candles_processed,
        provider,
        execution_time,
        analysis_status="Completed",
    ):
        """
        Updates the session after every completed scan.
        """

        self.last_scan = datetime.now()

        self.trend = trend
        self.signal = signal
        self.confidence = confidence

        self.candles_processed = candles_processed

        self.provider = provider

        self.execution_time = execution_time

        self.analysis_status = analysis_status

    def summary(self):
        """
        Returns session information for reporting.
        """

        return {
            "session_id": self.session_id,
            "market": self.market,
            "timeframe": self.timeframe,
            "started_at": self.started_at.strftime("%Y-%m-%d %H:%M:%S"),
            "last_scan": (
                self.last_scan.strftime("%Y-%m-%d %H:%M:%S")
                if self.last_scan
                else "None"
            ),
            "execution_time": f"{self.execution_time:.3f} sec",
            "provider": self.provider,
            "analysis_status": self.analysis_status,
            "candles_processed": self.candles_processed,
            "trend": self.trend,
            "signal": self.signal,
            "confidence": self.confidence,
        }