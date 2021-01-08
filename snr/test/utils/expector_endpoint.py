from snr.task import SomeTasks, Task
from snr.factory import Factory

from snr.test.utils.expector import Expector
from snr.endpoint.endpoint import Endpoint
from snr.node import Node


class ExpectorEndpoint(Endpoint):
    def __init__(self,
                 factory: Factory,
                 parent_node: Node,
                 expector: Expector
                 ) -> None:
        self.expector = expector
        task_handlers = {}
        for key in expector.expectations:
            task_handlers[key] = self.call
        super().__init__(factory,
                         parent_node,
                         "expector",
                         task_handlers=task_handlers)

    def call(self, task: Task) -> SomeTasks:
        self.expector.call(task.task_type)
        return None


class ExpectorEndpointFactory(Factory):
    def __init__(self, expector: Expector):
        super().__init__("Ping test factory")
        self.expector = expector

    def get(self, parent_node: Node) -> Endpoint:
        return ExpectorEndpoint(self,
                                parent_node,
                                self.expector)
