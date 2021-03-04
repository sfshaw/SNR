import logging
import unittest

from snr.types.base import *

from .expector_protocol import ExpectorProtocol

OrderedExpectations = List[Any]


class OrderedExpector(ExpectorProtocol):

    def __init__(self,
                 expectations: OrderedExpectations,
                 testcase: unittest.TestCase
                 ) -> None:
        self.log = logging.getLogger()
        self.log.setLevel(logging.WARNING)
        self.expectations = expectations
        self.testcase = testcase
        self.met_expectations: OrderedExpectations = []

    def get_expectations(self) -> Iterable[Any]:
        return self.expectations

    def call(self, key: Any) -> None:
        next_expectation = self.expectations[len(self.met_expectations)]
        if key == next_expectation:
            self.met_expectations.append(key)

    def assert_satisfied(self) -> None:
        '''Assert that all expectations have been satisfied
        '''
        if len(self.expectations) != len(self.met_expectations):
            self.dump()
        self.testcase.assertEqual(self.expectations, self.met_expectations)

    def check(self) -> bool:
        '''Check each expectation and shortcircuit if one is not satisfied.
        '''
        return self.expectations == self.met_expectations

    def dump(self) -> None:
        self.log.warning("Expected: %s \nGot %s",
                         self.expectations,
                         self.met_expectations)

    def __enter__(self) -> "OrderedExpector":
        return self
