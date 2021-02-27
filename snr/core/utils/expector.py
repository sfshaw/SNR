import logging
import unittest

from snr.types.base import *

from .expector_protocol import ExpectorProtocol

Expectations = Dict[Any, int]


class Expector(ExpectorProtocol):

    def __init__(self,
                 expectations: Expectations,
                 testcase: unittest.TestCase
                 ) -> None:
        self.expectations = expectations
        self.testcase = testcase
        self.log = logging.getLogger()
        self.times_called: Expectations = {}
        for key in expectations:
            self.times_called[str(key)] = 0

    def get_expectations(self) -> Iterable[Any]:
        return self.expectations.keys()

    def call(self, key: Any) -> None:
        val = self.times_called.get(str(key))
        if val is None:
            val = 0
        self.times_called[str(key)] = val + 1

    def assert_satisfied(self) -> None:
        '''Assert that all expectations have been satisfied
        '''
        for (key, expected_value) in self.expectations.items():
            if expected_value != self.times_called[str(key)]:
                self.dump()
            self.testcase.assertEqual(expected_value,
                                      self.times_called[str(key)],
                                      "For " + str(key))
        self.testcase.assertTrue(True)

    def check(self) -> bool:
        '''Check each expectation and shortcircuit if one is not satisfied.
        '''
        for (key, expected_value) in self.expectations.items():
            if expected_value != self.times_called[str(key)]:
                return False
        return True

    def dump(self) -> None:
        self.log.debug(self.times_called)

    def __enter__(self) -> "Expector":
        return self