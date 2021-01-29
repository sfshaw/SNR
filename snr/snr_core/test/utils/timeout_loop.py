import time

from snr.snr_core.base import *

FAST_TEST_TIMEOUT_MS: float = 10.0


class TimeoutLoop(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent_node: NodeProtocol,
                 timeout_s: float
                 ) -> None:
        super().__init__(factory,
                         parent_node,
                         "timeout_loop")
        self.timeout_s = timeout_s

    def setup(self) -> None:
        if self.timeout_s > 0:
            time.sleep(self.timeout_s)
        self.parent.schedule(task.terminate("Timeout"))


class TimeoutLoopFactory(LoopFactory):
    def __init__(self, seconds: float = 0, ms: float = 0):
        super().__init__("Timeout loop factory")
        self.timeout_s = seconds + (ms / 1000)

    def get(self, parent: NodeProtocol) -> LoopProtocol:
        return TimeoutLoop(self,
                           parent,
                           self.timeout_s)
