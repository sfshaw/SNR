import unittest
from sys import stdout
from typing import List

from snr_core.config import Config, Mode
from snr_core.context.stdout import StdOut
from snr_core.factory.factory_base import FactoryBase


class SNRTestBase(unittest.TestCase):

    def setUp(self) -> None:
        print()
        stdout.flush()
        self.stdout: StdOut = StdOut(self.id(), None)

    def tearDown(self) -> None:
        self.stdout.join_from("test_teardown")

    def get_config(self,
                   factories: List[FactoryBase],
                   mode: Mode = Mode.TEST
                   ) -> Config:
        if mode is Mode.DEBUG and not self.stdout.stdout:
            self.stdout.stdout = stdout
        return Config(mode, {"test": factories}, self.stdout)
