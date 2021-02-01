import time

from snr.snr_core.base import *


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
