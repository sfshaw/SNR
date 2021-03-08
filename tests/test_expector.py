import multiprocessing as mp
import unittest

from snr import *


class TestExpector(unittest.TestCase):

    def test_empty(self):
        expector = Expector({}, self)
        expector.assert_satisfied()

    def test_empty_with_syntax(self):
        with Expector({}, self) as _:
            pass

    def test_call(self):
        with Expector({
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
            with Expector({
                "foop": 1
            },
                    self) as _:
                pass

    def test_expector_proc(self) -> None:
        expectations: Expectations = {
            "called": 1
        }
        with MPExpector(expectations, self) as expector:
            def call():
                expector.call("called")

            proc = mp.Process(target=call)
            proc.start()
            proc.join()
