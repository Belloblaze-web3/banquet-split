import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOLUTION = ROOT / "solution.py"


def run_case(input_text):
    completed = subprocess.run(
        [sys.executable, str(SOLUTION)],
        input=input_text,
        text=True,
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip().splitlines()


class BanquetSplitTests(unittest.TestCase):
    def test_sample_case(self):
        sample = """\
1
5
1 2
1 3
3 4
3 5
2
2 4
1 5
"""
        self.assertEqual(run_case(sample), ["Yes", "No", "1 3"])

    def test_adjacent_vertices_are_possible(self):
        data = """\
1
3
1 2
2 3
2
1 2
2 3
"""
        self.assertEqual(run_case(data), ["Yes", "Yes"])

    def test_same_vertex_requires_one_removal(self):
        data = """\
1
3
1 2
2 3
1
2 2
"""
        self.assertEqual(run_case(data), ["No", "1 1"])

    def test_longer_even_path_reports_cycle_length(self):
        data = """\
1
4
1 2
2 3
3 4
2
1 3
1 4
"""
        self.assertEqual(run_case(data), ["No", "1 3", "Yes"])


if __name__ == "__main__":
    unittest.main()
