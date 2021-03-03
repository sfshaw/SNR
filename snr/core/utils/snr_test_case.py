import socket
import threading
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

    def tearDown(self) -> None:
        t = time.time() - self.startTime
        if PRINT_INDIVIDUAL_RUNTIME:
            print(f"{self.id()}: \t{t:32.3f}s")
        for thread in threading.enumerate():
            if not thread.is_alive():
                print("Zombie thread %s culled", thread.name)

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

    def get_context(self) -> ContextProtocol:
        return RootContext("test_context", None)

    def run_test_node(self,
                      factories: List[FactoryProtocol],
                      mode: Mode = Mode.TEST
                      ) -> None:
        config = self.get_config(factories, mode)
        runner = TestRunner(config)
        runner.run()

    def mock_node(self) -> NodeProtocol:
        return MockNode()

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
        self.assertTrue(isinstance(page, Page))
        assert isinstance(page, Page)
        self.assertEqual(key, page.key)
        self.assertEqual(data, page.data)
        self.assertEqual(origin, page.origin)
        if created_at:
            self.assertAlmostEqual(created_at, page.created_at_s)
        self.assertEqual(process, page.process)

    def create_server(self, addr: Tuple[str, int],
                      timeout_s: Optional[float] = None,
                      ) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        if timeout_s:
            sock.settimeout(timeout_s)
        sock.bind(addr)
        sock.listen(10)
        return sock
