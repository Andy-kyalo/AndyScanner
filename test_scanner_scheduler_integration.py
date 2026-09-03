import unittest

from backend.scanner.scanner_job import ScannerJob
from backend.scanner.scanner_queue import ScannerQueue


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

        self.assertEqual(
            len(ready),
            1,
        )

        self.assertIs(
            ready[0],
            job,
        )


if __name__ == "__main__":
    unittest.main()
