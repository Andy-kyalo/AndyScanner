import unittest

from backend.scanner.scanner_job import ScannerJob
from backend.scanner.scanner_queue import ScannerQueue
from backend.scanner.scanner_executor import ScannerExecutor
from backend.scanner.scanner_scheduler import ScannerScheduler


class FakeManager:

    def __init__(self):
        self.calls = []

    def run(self, market, timeframe):
        self.calls.append((market, timeframe))

        return {
            "market": market,
            "timeframe": timeframe,
        }


class TestScannerSchedulerIntegration(unittest.TestCase):

    def test_job_ready_property(self):
        job = ScannerJob(
            market="US30",
            timeframe="M5",
        )

        self.assertTrue(job.ready)

    def test_queue_returns_ready_job(self):
        queue = ScannerQueue()

        job = ScannerJob(
            market="US30",
            timeframe="M5",
        )

        self.assertTrue(queue.add(job))

        ready = queue.ready_jobs()

        self.assertEqual(len(ready), 1)
        self.assertIs(ready[0], job)

    def test_scheduler_executes_ready_queue(self):
        manager = FakeManager()
        executor = ScannerExecutor(manager)
        queue = ScannerQueue()

        job = ScannerJob(
            market="US30",
            timeframe="M5",
        )

        self.assertTrue(queue.add(job))

        scheduler = ScannerScheduler(
            queue=queue,
            executor=executor,
        )

        results = scheduler.run_queue()

        self.assertEqual(len(results), 1)
        self.assertEqual(
            manager.calls,
            [("US30", "M5")],
        )

        self.assertEqual(
            executor.total_executions,
            1,
        )

        self.assertEqual(
            executor.successful_executions,
            1,
        )

        self.assertEqual(
            executor.failed_executions,
            0,
        )


if __name__ == "__main__":
    unittest.main()