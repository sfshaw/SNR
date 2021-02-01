from snr.snr_core.base import *

from . import timeout_loop

FAST_TEST_TIMEOUT_MS: float = 10.0


class TimeoutLoopFactory(LoopFactory):
    def __init__(self, seconds: float = 0, ms: float = 0):
        super().__init__(timeout_loop)
        self.timeout_s = seconds + (ms / 1000)

    def get(self, parent: NodeProtocol) -> LoopProtocol:
        return timeout_loop.TimeoutLoop(self,
                                        parent,
                                        self.timeout_s)
