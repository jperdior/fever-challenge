"""Test cases for DateRangeVo value object."""

import unittest
from datetime import datetime
from src.shared.domain.vo import DateRangeVo


class TestDateRangeVo(unittest.TestCase):

    def test_valid_date_range(self):
        """Should create a valid date range."""
        date_range = DateRangeVo("2023-01-01T00:00:00", "2023-01-02T00:00:00")
        self.assertEqual(date_range.start_date, "2023-01-01")
        self.assertEqual(date_range.end_date, "2023-01-02")
        self.assertEqual(date_range.start_time, "00:00:00")
        self.assertEqual(date_range.end_time, "00:00:00")

    def test_invalid_date_format(self):
        """Should raise ValueError when date format is invalid."""
        with self.assertRaises(ValueError):
            DateRangeVo("2023-01-01", "2023-01-02T00:00:00")

    def test_start_date_after_end_date(self):
        """Should raise ValueError when start date is after end date."""
        with self.assertRaises(ValueError):
            DateRangeVo("2023-01-02T00:00:00", "2023-01-01T00:00:00")


if __name__ == "__main__":
    unittest.main()
