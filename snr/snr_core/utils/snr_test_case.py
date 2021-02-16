import time
import unittest

from ..base import *
from ..context.root_context import RootContext
from .expector import Expectations, Expector
from .expector_protocol import ExpectorProtocol
from .mock_node import MockNode
from .ordered_expector import OrderedExpectations, OrderedExpector
from .temp_file import TempFile

PRINT_INDIVIDUAL_RUNTIME: bool = True


class SNRTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.startTime = time.time()
        self.test_name = self.id().split(".")[-1]
        self.root_context = RootContext(self.test_name)
        self.log = self.root_context.log

    def tearDown(self) -> None:
        t = time.time() - self.startTime
        if PRINT_INDIVIDUAL_RUNTIME:
            print(f"{self.id()}: \t{t:32.3f}s")

    def context(self):
        return Context(self.id(), self.root_context)

    def expector(self,
                 expectations: Expectations
                 ) -> ExpectorProtocol:
        return Expector(expectations, self)

    def ordered_expector(self,
                         expectations: OrderedExpectations
                         ) -> ExpectorProtocol:
        return OrderedExpector(expectations, self)

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
        runner = TestRunner(config)
        runner.run()

    def mock_node(self) -> NodeProtocol:
        return MockNode(self.root_context)

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
            self.assertTrue(False, "Given page is not a Page")
