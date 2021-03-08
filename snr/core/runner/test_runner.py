from snr.protocol import *

from .synchronous_runner import SynchronousRunner


class TestRunner(SynchronousRunner):
    __test__ = False

    def __init__(self,
                 config: ConfigProtocol,
                 ) -> None:
        super().__init__("test", config)
