import logging
from unittest.case import TestCase

from snr.snr_types.base import *

Expectations = Dict[Any, int]


class Expector:
    def __init__(self, expectations: Expectations, testcase: TestCase) -> None:
        self.expectations = expectations
        self.testcase = testcase
        self.log = logging.getLogger()
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

    def check(self) -> bool:
        """Safety failable version of assertSatisfied, can be called
        and fail without raising AssertionError
        """
        for (key, expected_value) in self.expectations.items():
            if expected_value != self.times_called[str(key)]:
                return False
        return True

    def dump(self) -> None:
        self.log.debug(self.times_called)

    def __enter__(self) -> "Expector":
        return self

    def __exit__(self, *args: Any) -> None:
        self.assert_satisfied()
