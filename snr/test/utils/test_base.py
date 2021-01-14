import unittest
from sys import stdout
from typing import List

from snr.config import Config, Mode
from snr.context.silent_stdout import SilentStdOut
from snr.context.stdout import StdOut
from snr.context.stdout_consumer import StdOutConsumer
from snr.endpoint.factory import Factory


class SNRTestBase(unittest.TestCase):

    def setUp(self) -> None:
        print()
        stdout.flush()
        self.stdout: StdOutConsumer = SilentStdOut(self.id())

    def tearDown(self) -> None:
        self.stdout.join_from("test_teardown")

    def get_config(self, factories: List[Factory]) -> Config:
        return Config(Mode.TEST, {"test": factories}, self.stdout)
