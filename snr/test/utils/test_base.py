import unittest
from sys import stdout

from snr.context.stdout import StdOut


class SNRTestBase(unittest.TestCase):

    def setUp(self) -> None:
        print()
        stdout.flush()
        self.stdout = StdOut(self.id())

    def tearDown(self) -> None:
        self.stdout.join_from("test_teardown")
