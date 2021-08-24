from snr.prelude import *

from .synchronous_runner import SynchronousRunner


class TestRunner(SynchronousRunner):
    __test__ = False

    def __init__(self,
                 config: AbstractConfig,
                 ) -> None:
        super().__init__("test", config)
