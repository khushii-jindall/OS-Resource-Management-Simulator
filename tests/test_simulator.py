
import unittest
from io import StringIO
from contextlib import redirect_stdout

from modules.cpu_scheduling import fcfs, sjf, round_robin
from modules.memory_management import first_fit, best_fit, worst_fit
from modules.deadlock import is_safe_state
from modules.disk_scheduling import (
    fcfs as disk_fcfs,
    sstf,
    scan
)


class TestCPUScheduling(unittest.TestCase):

    def setUp(self):
        self.processes = [
            {"pid": "P1", "arrival": 0, "burst": 5},
            {"pid": "P2", "arrival": 1, "burst": 3},
            {"pid": "P3", "arrival": 2, "burst": 1},
            {"pid": "P4", "arrival": 3, "burst": 2},
        ]

    def test_fcfs(self):
        self.assertIsNotNone(fcfs(self.processes))

    def test_sjf(self):
        self.assertIsNotNone(sjf(self.processes))

    def test_round_robin(self):
        self.assertIsNotNone(round_robin(self.processes, 2))


class TestMemoryManagement(unittest.TestCase):

    def setUp(self):
        self.blocks = [100, 500, 200, 300, 600]
        self.processes = [212, 417, 112, 426]

    def capture_output(self, function):
        output = StringIO()
        with redirect_stdout(output):
            result = function(self.blocks, self.processes)

        # Input lists should not be modified.
        self.assertEqual(self.blocks, [100, 500, 200, 300, 600])
        self.assertEqual(self.processes, [212, 417, 112, 426])

        return result, output.getvalue()

    def test_first_fit(self):
        _, output = self.capture_output(first_fit)

        self.assertIn("P1          212         B2", output)
        self.assertIn("P2          417         B5", output)
        self.assertIn("P3          112         B2", output)
        self.assertIn("P4          426         -", output)
        self.assertIn("Processes allocated: 3/4", output)
        self.assertIn("Block B2: 176 units", output)
        self.assertIn("Block B5: 183 units", output)

    def test_best_fit(self):
        _, output = self.capture_output(best_fit)

        self.assertIn("P1          212         B4", output)
        self.assertIn("P2          417         B2", output)
        self.assertIn("P3          112         B3", output)
        self.assertIn("P4          426         B5", output)
        self.assertIn("Processes allocated: 4/4", output)
        self.assertIn("Block B2: 83 units", output)
        self.assertIn("Block B5: 174 units", output)

    def test_worst_fit(self):
        _, output = self.capture_output(worst_fit)

        self.assertIn("P1          212         B5", output)
        self.assertIn("P2          417         B2", output)
        self.assertIn("P3          112         B5", output)
        self.assertIn("P4          426         -", output)
        self.assertIn("Processes allocated: 3/4", output)
        self.assertIn("Block B2: 83 units", output)
        self.assertIn("Block B5: 276 units", output)


class TestDeadlockAvoidance(unittest.TestCase):

    def test_safe_state(self):
        available = [3, 3, 2]

        allocation = [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2],
        ]

        maximum = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3],
        ]

        safe, sequence, need = is_safe_state(
            available, allocation, maximum
        )

        self.assertTrue(safe)
        self.assertEqual(len(sequence), 5)
        self.assertEqual(len(need), 5)


class TestDiskScheduling(unittest.TestCase):

    def setUp(self):
        self.requests = [98, 183, 37, 122, 14, 124, 65, 67]
        self.head = 53

    def test_fcfs(self):
        self.assertIsNotNone(disk_fcfs(self.requests, self.head))

    def test_sstf(self):
        self.assertIsNotNone(sstf(self.requests, self.head))

    def test_scan(self):
        self.assertIsNotNone(scan(self.requests, self.head))


if __name__ == "__main__":
    unittest.main(verbosity=2)
