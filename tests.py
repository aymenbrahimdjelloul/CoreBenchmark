# @author : Aymen Brahim Djelloul
# date : 02.09.2024
# License : MIT

# IMPORTS
import unittest
from core_benchmark import CoreBenchmark  # Assuming your main file is named core_benchmark.py
from decimal import Decimal


class TestCoreBenchmark(unittest.TestCase):

    def setUp(self):
        """
        Set up the CoreBenchmark instance before every test.
        """
        self.benchmark = CoreBenchmark()

    def test_pi_calculation(self):
        """
        Test the private method _calculate_pi to ensure correct chunk calculation.
        """
        pi_chunk = self.benchmark._calculate_pi(100, 0)
        self.assertIsInstance(pi_chunk, Decimal, "The result should be a Decimal representing pi chunk.")
        self.assertGreater(pi_chunk, 0, "Pi chunk should be a positive value.")

    def test_calculate_score(self):
        """
        Test the score calculation method to ensure it returns a correct score.
        """
        score = self.benchmark._calculate_score(5.0)
        self.assertEqual(score, 1667,
                         "Score should match the expected value for time_taken=5.0, scale=10000, offset=1.")

    def test_multi_core_benchmark(self):
        """
        Test the multi-core benchmark method to ensure it runs and returns a result.
        """
        result = self.benchmark.benchmark_all_cores(score_result=False)
        self.assertIsInstance(result, float, "The result should be a float representing time.")
        self.assertGreater(result, 0, "Multi-core benchmark time should be greater than zero.")

    def tearDown(self):
        """
        Clean up after every test.
        """
        del self.benchmark


if __name__ == "__main__":
    unittest.main()
