import unittest
from sys import stdout
from typing import List, Optional

from snr_core.config import Config, Mode
from snr_core.context.context import Context
from snr_core.context.root_context import RootContext
from snr_core.factory.factory_protocol import FactoryProtocol
from snr_core.runner.test_runner import SynchronusTestRunner
from snr_core.test.utils.expector import Expectations, Expector
from snr_core.test.utils.temp_file import TempFile


class SNRTestBase(unittest.TestCase):

    def setUp(self) -> None:
        stdout.flush()
        self.test_name = self.id().split(".")[-1]
        self.root_context = RootContext(self.test_name)

    def tearDown(self) -> None:
        pass

    def context(self):
        return Context(self.id(), self.root_context)

    def expector(self, expectations: Expectations) -> Expector:
        return Expector(expectations, self)

    def get_config(self,
                   factories: List[FactoryProtocol],
                   mode: Mode = Mode.TEST
                   ) -> Config:
        return Config(mode, {"test": factories})

    def run_test(self,
                 factories: List[FactoryProtocol],
                 mode: Mode = Mode.TEST
                 ) -> None:
        config = self.get_config(factories, mode)
        runner = SynchronusTestRunner(config)
        runner.run()

    def temp_file(self,
                  filename: Optional[str] = None,
                  overwrite: bool = False,
                  cleanup: bool = True):
        if not filename:
            filename = self.test_name + ".tmp"
        return TempFile(self, filename, overwrite, cleanup)
