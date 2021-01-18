from __future__ import annotations

from typing import Any, Dict
from unittest.case import TestCase

Expectations = Dict[Any, int]


class Expector:
    def __init__(self, expectations: Expectations, testcase: TestCase) -> None:
        self.expectations = expectations
        self.testcase = testcase
        self.times_called: Expectations = {}
        for key in expectations:
            self.times_called[str(key)] = 0

    def call(self, key: Any):
        val = self.times_called.get(str(key))
        if val is None:
            val = 0
        self.times_called[str(key)] = val + 1

    def assert_satisfied(self):
        for (key, expected_value) in self.expectations.items():
            if expected_value != self.times_called[str(key)]:
                self.dump()
            self.testcase.assertEqual(expected_value,
                                      self.times_called[str(key)],
                                      "For " + str(key))
        self.testcase.assertTrue(True)

    def dump(self) -> None:
        print(self.times_called)

    def __enter__(self) -> Expector:
        return self

    def __exit__(self, *args: Any) -> None:
        self.assert_satisfied()
