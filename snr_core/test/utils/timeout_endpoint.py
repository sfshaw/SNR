from snr_core import task
from snr_core.loop.loop_base import LoopBase
from snr_core.loop.loop_factory import LoopFactory
from snr_core.loop.thread_loop import ThreadLoop
from snr_core.node import Node
from snr_core.utils.utils import no_op


class TimeoutEndpoint(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent_node: Node,
                 timeout_s: float
                 ) -> None:
        super().__init__(factory,
                         parent_node,
                         "timeout_endpoint",
                         no_op)
        self.timeout_s = timeout_s

    def setup(self) -> None:
        self.sleep(self.timeout_s)
        self.parent_node.schedule(task.terminate("Timeout"))


class TimeoutEndpointFactory(LoopFactory):
    def __init__(self, seconds: float = 0, ms: float = 0):
        super().__init__("Ping test factory")
        self.timeout_s = seconds + (ms / 1000)

    def get(self, parent: Node) -> LoopBase:
        return TimeoutEndpoint(self,
                               parent,
                               self.timeout_s)
