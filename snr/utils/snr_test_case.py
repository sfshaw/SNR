import socket
import time
import unittest
from typing import Any, List, Mapping, Optional, Tuple

from snr.core import *
from snr.prelude import *
from snr.std_mods import *

from .expector import Expector
from .expector_protocol import ExpectorProtocol
from .mock_node import MockNode
from .ordered_expector import OrderedExpector

PRINT_INDIVIDUAL_RUNTIME: bool = True


class SNRTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.startTime = time.time()
        self.test_name = self.id().split(".")[-1]
        self.temp_files_used = 0

    def tearDown(self) -> None:
        if PRINT_INDIVIDUAL_RUNTIME:
            end_time = time.time() - self.startTime
            print(f"{end_time* 1000:6.2f} ms: {self.id()}")

    def expector(self,
                 expectations: Mapping[Any, int],
                 ) -> ExpectorProtocol:
        return Expector(expectations, self)

    def ordered_expector(self,
                         expectations: List[Any],
                         ) -> ExpectorProtocol:
        return OrderedExpector(expectations, self)

    def get_config(self,
                   factories: List[AbstractFactory[Any]] = [],
                   mode: Mode = Mode.TEST
                   ) -> Config:
        return Config(mode, {"test": factories})

    def get_context(self) -> AbstractContext:
        return RootContext("test_context", Mode.TEST)

    def run_test_node(self,
                      factories: List[AbstractFactory[Any]],
                      mode: Mode = Mode.TEST,
                      ) -> None:
        config = self.get_config(factories, mode)
        runner = TestRunner(config)
        runner.run()

    def mock_node(self) -> AbstractNode:
        return MockNode()

    def temp_file(self,
                  filename: Optional[str] = None,
                  overwrite: bool = False,
                  cleanup: bool = True,
                  ) -> TempFile:
        if not filename:
            filename = f"{self.test_name}_{self.temp_files_used}.tmp"
            self.temp_files_used += 1
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

    def wrap_socket(self,
                    connection: Tuple[socket.socket, Any],
                    ) -> SocketsWrapper:
        return SocketsWrapper(connection, self.get_context())
