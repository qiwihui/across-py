from dataclasses import dataclass
import unittest
from across.utils import sorted_index_by


class TestFeeCalculator(unittest.TestCase):
    def test_sorted_index_by(self):
        @dataclass
        class SimpleObj:
            x: int

        data = (
            [[{"x": 1}, {"x": 4}, {"x": 5}], 4, "x", 1],
            [[{"x": 1}, {"x": 3}, {"x": 5}], 4, "x", 2],
            [[{"x": 1}, {"x": 3}, {"x": 5}], 0, "x", 0],
            [[{"x": 1}, {"x": 3}, {"x": 5}], 6, "x", 3],
            [[1, 4, 5], 4, None, 1],
            [[SimpleObj(1), SimpleObj(3), SimpleObj(5)], 4, "x", 2],
        )
        for i in range(len(data)):
            self.assertEqual(
                sorted_index_by(data[i][0], data[i][1], data[i][2]), data[i][3]
            )
