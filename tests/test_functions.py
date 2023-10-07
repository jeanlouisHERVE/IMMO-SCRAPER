import unittest
from modules.functions import (
    date_converter_french_date_to_utc_timestamp,
    contains_numbers,
    are_timestamps_equal
)


class TestFunctions(unittest.TestCase):
    def test_date_converter_french_date_to_utc_timestamp(self):
        # Test case 1: valid input
        french_date = "15 août 2023"
        expected_timestamp = 1692057600.0  # Expected UTC timestamp
        result = date_converter_french_date_to_utc_timestamp(french_date)
        self.assertAlmostEqual(result, expected_timestamp, places=2)

        # Test case 2: invalid input with non-existent month
        french_date = "20 décembrrr 2023"
        result = date_converter_french_date_to_utc_timestamp(french_date)
        self.assertIsNone(result)  # Expecting None

    def test_contains_numbers(self):
        # Test case 1: input contains numbers
        input_string = "This is a string with 12345 numbers."
        result = contains_numbers(input_string)
        self.assertTrue(result)  # Expecting True

        # Test case 2: input does not contain numbers
        input_string = "No numbers here."
        result = contains_numbers(input_string)
        self.assertFalse(result)  # Expecting False

    def test_are_timestamps_equal(self):
        # Test case 1: timestamps are equal within the tolerance
        timestamp1 = 100.0
        timestamp2 = 101.0
        tolerance_seconds = 2
        result = are_timestamps_equal(timestamp1, timestamp2, tolerance_seconds)
        self.assertTrue(result)  # Expecting True

        # Test case 2: timestamps are not equal within the tolerance
        timestamp1 = 100.0
        timestamp2 = 120.0
        tolerance_seconds = 10
        result = are_timestamps_equal(timestamp1, timestamp2, tolerance_seconds)
        self.assertFalse(result)  # Expecting False


if __name__ == '__main__':
    unittest.main()

# Define the order of tests
    ordered_tests = [
        "test_date_converter_french_date_to_utc_timestamp",
        "test_contains_numbers",
        "test_are_timestamps_equal",
    ]

    test_instance = TestFunctions()
    ordered_suite = unittest.TestSuite()

    for test_name in ordered_tests:
        ordered_suite.addTest(test_instance.findTest(test_instance, test_name))

    runner = unittest.TextTestRunner()
    runner.run(ordered_suite)
