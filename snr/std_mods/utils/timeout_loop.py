import time

from snr.core import *
from snr.prelude import *


class TimeoutLoop(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent_node: AbstractNode,
                 timeout_s: float,
                 task: Task,
                 ) -> None:
        super().__init__(factory,
                         parent_node,
                         "timeout_loop")
        self.timeout_s = timeout_s
        self.task = task

    def setup(self) -> None:
        if self.timeout_s > 0:
            time.sleep(self.timeout_s)
        self.parent.schedule(self.task)

    def loop(self) -> None:
        pass

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass
