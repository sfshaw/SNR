from snr_core.endpoint.endpoint_factory import EndpointFactory
from snr_core.endpoint.factory import Factory
from snr_core.endpoint.synchronous_endpoint import SynchronousEndpoint
from snr_core.node import Node
from snr_core.task import SomeTasks, Task
from snr_core.test.utils.expector import Expector


class ExpectorEndpoint(SynchronousEndpoint):
    def __init__(self,
                 factory: Factory,
                 parent_node: Node,
                 expector: Expector
                 ) -> None:
        task_handlers = {}
        for key in expector.expectations:
            task_handlers[key] = self.call
        super().__init__(factory,
                         parent_node,
                         "expector",
                         task_handlers=task_handlers)
        self.expector = expector

    def call(self, task: Task) -> SomeTasks:
        self.dbg(f"Expector called for: {task}")
        self.expector.call(task.type)
        return None


class ExpectorEndpointFactory(EndpointFactory):
    def __init__(self, expector: Expector):
        super().__init__("Ping test factory")
        self.expector = expector

    def get(self, parent: Node) -> SynchronousEndpoint:
        return ExpectorEndpoint(self,
                                parent,
                                self.expector)
