import unittest
from sys import stdout
from typing import List

from snr_core.config import Config, Mode
from snr_core.context.silent_stdout import SilentStdOut
from snr_core.context.stdout_consumer import StdOutConsumer
from snr_core.endpoint.factory import Factory


class SNRTestBase(unittest.TestCase):

    def setUp(self) -> None:
        print()
        stdout.flush()
        self.stdout: StdOutConsumer = SilentStdOut(self.id())

    def tearDown(self) -> None:
        self.stdout.join_from("test_teardown")

    def get_config(self, factories: List[Factory]) -> Config:
        return Config(Mode.TEST, {"test": factories}, self.stdout)
