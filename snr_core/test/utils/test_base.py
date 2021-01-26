import unittest
from sys import stdout
from typing import List

from snr_core.config import Config, Mode
from snr_core.context.context import Context
from snr_core.context.root_context import RootContext
from snr_core.factory.factory_base import FactoryBase
from snr_core.runner.test_runner import SynchronusTestRunner
from snr_core.test.utils.expector import Expectations, Expector


class SNRTestBase(unittest.TestCase):

    def setUp(self) -> None:
        stdout.flush()
        self.root_context = RootContext(self.id())

    def context(self):
        return Context(self.id(), self.root_context)

    def expector(self, expectations: Expectations) -> Expector:
        return Expector(expectations, self)

    def get_config(self,
                   factories: List[FactoryBase],
                   mode: Mode = Mode.TEST
                   ) -> Config:
        return Config(mode, {"test": factories})

    def run_test(self,
                 factories: List[FactoryBase],
                 mode: Mode = Mode.TEST
                 ) -> None:
        config = self.get_config(factories, mode)
        runner = SynchronusTestRunner(config)
        runner.run()
