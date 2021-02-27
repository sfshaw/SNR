import unittest

from snr.types.base import *

Expectations = Dict[Any, int]


@runtime_checkable
class ExpectorProtocol(Protocol):
    testcase: unittest.TestCase

    def get_expectations(self) -> Iterable[Any]:
        '''View the expector's expectations so they can be used
        to match tasks for task handlers
        '''
        ...

    def call(self, key: Any) -> None:
        '''Complete an action to possibly satisfy an expectation
        '''
        ...

    def assert_satisfied(self):
        '''Assert in the context of a unittest.TestCase, that all
        expectations were met.
        '''
        ...

    def check(self) -> bool:
        """Safety failable version of assert_satisfied, can be called
        and fail without raising AssertionError.
        """
        ...

    def __enter__(self) -> "ExpectorProtocol":
        ...

    def __exit__(self, *args: Any) -> None:
        self.assert_satisfied()
