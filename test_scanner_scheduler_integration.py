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
    def test_timeframe_intervals(self):
        m1 = ScannerJob(
            market="US30",
            timeframe="M1",
        )

        m5 = ScannerJob(
            market="US30",
            timeframe="M5",
        )

        m15 = ScannerJob(
            market="US30",
            timeframe="M15",
        )

        self.assertEqual(m1.interval, 60)
        self.assertEqual(m5.interval, 300)
        self.assertEqual(m15.interval, 900)
    def test_explicit_interval_overrides_timeframe(self):
        job = ScannerJob(
            market="US30",
            timeframe="M5",
            interval=120,
        )

        self.assertEqual(job.interval, 120)
    def test_next_run_uses_timeframe_interval(self):
        job = ScannerJob(
            market="US30",
            timeframe="M5",
        )

        before = job.created_at

        job.mark_success()

        self.assertEqual(job.interval, 300)
        self.assertIsNotNone(job.last_run)
        self.assertGreaterEqual(
            job.next_run,
            job.last_run,
        )
        self.assertEqual(
            (job.next_run - job.last_run).total_seconds(),
            300,
        )
        self.assertGreaterEqual(
            job.last_run,
            before,
        )


if __name__ == "__main__":
    unittest.main()
