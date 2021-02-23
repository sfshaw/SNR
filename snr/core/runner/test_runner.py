from snr.protocol import *

from ..runner.synchronus_runner import SynchronousRunner


class TestRunner(SynchronousRunner):
    __test__ = False

    def __init__(self,
                 config: ConfigProtocol
                 ) -> None:
        super().__init__("test", config)
