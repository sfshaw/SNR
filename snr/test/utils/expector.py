from typing import Dict
import unittest

Expectations = Dict[str, int]


class Expector:
    def __init__(self, expectations: Expectations) -> None:
        self.expectations = expectations
        self.times_called: Expectations = {}
        for key in expectations:
            self.times_called[key] = 0

    def call(self, key: str):
        val = self.times_called.get(key)
        if val is None:
            val = 0
        self.times_called[key] = val + 1

    def assert_satisfied(self, testcase: unittest.TestCase):
        for (key, expected_value) in self.expectations.items():
            testcase.assertEqual(expected_value,
                                 self.times_called[key],
                                 "For " + key)
        testcase.assertTrue(True)
