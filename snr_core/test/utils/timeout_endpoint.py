from snr_core import task
from snr_core.endpoint.endpoint import Endpoint
from snr_core.endpoint.endpoint_factory import EndpointFactory
from snr_core.endpoint.factory import Factory
from snr_core.endpoint.thread_endpoint import ThreadEndpoint
from snr_core.node import Node
from snr_core.utils.utils import no_op


class TimeoutEndpoint(ThreadEndpoint):
    def __init__(self,
                 factory: Factory,
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


class TimeoutEndpointFactory(EndpointFactory):
    def __init__(self, seconds: float = 0, ms: float = 0):
        super().__init__("Ping test factory")
        self.timeout_s = seconds + (ms / 1000)

    def get(self, parent: Node) -> Endpoint:
        return TimeoutEndpoint(self,
                               parent,
                               self.timeout_s)
