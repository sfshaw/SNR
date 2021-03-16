import multiprocessing as mp
from typing import Any, Mapping
import unittest

from snr import *


class TestExpector(unittest.TestCase):

    def test_empty(self):
        expector = Expector[Any]({}, self)
        expector.assert_satisfied()

    def test_empty_with_syntax(self):
        with Expector[Any]({}, self) as _:
            pass

    def test_call(self):
        with Expector[str]({
            "foo": 0,
            "bar": 1,
            "bazz": 2
        },
                self) as expector:
            expector.call("bar")
            expector.call("bazz")
            expector.call("bazz")
            expector.call("extraneous")

    def test_fail(self):
        with self.assertRaises(AssertionError):
            with Expector[Any]({
                "foop": 1
            }, self) as _:
                pass

    def test_expector_proc(self) -> None:
        expectations: Mapping[str, int] = {
            "called": 1
        }
        with MPExpector[str](expectations, self) as expector:
            def call():
                expector.call("called")

            proc = mp.Process(target=call)
            proc.start()
            proc.join()
