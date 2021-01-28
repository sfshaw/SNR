import unittest
from sys import stdout
from typing import List, Optional

from snr_core.config import Config
from snr_core.context.context import Context
from snr_core.context.root_context import RootContext
from snr_core.protocols import *
from snr_core.runner.test_runner import SynchronusTestRunner
from snr_core.test.utils.expector import Expectations, Expector
from snr_core.test.utils.temp_file import TempFile
from snr_types import *


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

    def run_test_node(self,
                      factories: List[FactoryProtocol],
                      mode: Mode = Mode.TEST
                      ) -> None:
        config = self.get_config(factories, mode)
        runner = SynchronusTestRunner(config)
        runner.run()

    def temp_file(self,
                  filename: Optional[str] = None,
                  overwrite: bool = False,
                  cleanup: bool = True
                  ) -> TempFile:
        if not filename:
            filename = self.test_name + ".tmp"
        return TempFile(self, filename, overwrite, cleanup)

    def assertPage(self, page: Optional[Page],
                   key: DataKey,
                   data: Any,
                   origin: str,
                   created_at: Optional[float] = None,
                   process: bool = True):
        if page:
            self.assertEqual(key, page.key)
            self.assertEqual(data, page.data)
            self.assertEqual(origin, page.origin)
            if created_at:
                self.assertAlmostEqual(created_at, page.created_at)
            self.assertEqual(process, page.process)
        else:
            self.assertTrue(False, f"{page} is not a Page")
