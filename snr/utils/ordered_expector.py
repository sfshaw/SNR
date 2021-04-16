import logging
import unittest
from typing import Any, Generic, List, TypeVar

from snr.type_defs import *

from .expector_protocol import ExpectorProtocol

T = TypeVar('T')


class OrderedExpector(ExpectorProtocol, Generic[T]):

    def __init__(self,
                 expectations: List[T],
                 testcase: unittest.TestCase
                 ) -> None:
        self.log = logging.getLogger()
        self.log.setLevel(logging.WARNING)
        self.expectations = expectations
        self.testcase = testcase
        self.met_expectations: List[str] = []

    def get_expectations(self) -> List[T]:
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

    def __enter__(self) -> "OrderedExpector[T]":
        return self
