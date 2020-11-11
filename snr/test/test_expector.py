import unittest

from snr.test.expector import Expector


class TestExpector(unittest.TestCase):

    def test_empty(self):
        expector = Expector({})
        expector.assert_satisfied(self)

    def test_call(self):
        expector = Expector({
            "foo": 0,
            "bar": 1,
            "bazz": 2
        })
        expector.call("bar")
        expector.call("bazz")
        expector.call("bazz")
        expector.call("extraneous")
        expector.assert_satisfied(self)

    def test_fail(self):
        expector = Expector({
            "foop": 1
        })
        with self.assertRaises(AssertionError):
            expector.assert_satisfied(self)


if __name__ == '__main__':
    unittest.main()
