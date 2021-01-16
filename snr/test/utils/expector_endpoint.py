from snr.endpoint.endpoint_factory import EndpointFactory
from snr.endpoint.factory import Factory
from snr.endpoint.synchronous_endpoint import SynchronousEndpoint
from snr.node import Node
from snr.task import SomeTasks, Task
from snr.test.utils.expector import Expector


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
        print(f"Called for: {task}")
        self.expector.call(task.id())
        return None


class ExpectorEndpointFactory(EndpointFactory):
    def __init__(self, expector: Expector):
        super().__init__("Ping test factory")
        self.expector = expector

    def get(self, parent: Node) -> SynchronousEndpoint:
        return ExpectorEndpoint(self,
                                parent,
                                self.expector)
