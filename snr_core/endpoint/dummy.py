from snr.endpoint.endpoint import Endpoint
from snr.endpoint.synchronous_endpoint import SynchronousEndpoint
from snr.endpoint.factory import Factory
from snr.node import Node
from snr.task import TaskHandlerMap

DEFAULT_NAME = "dummy_endpoint"


class DummyEndpoint(SynchronousEndpoint):
    def __init__(self,
                 factory: Factory,
                 parent: Node,
                 name: str = DEFAULT_NAME,
                 task_handlers: TaskHandlerMap = {}):
        super().__init__(factory,
                         parent,
                         name,
                         task_handlers=task_handlers)


class DummyEndpointFactory(Factory):
    def __init__(self,
                 name: str = DEFAULT_NAME,
                 task_handlers: TaskHandlerMap = {}
                 ) -> None:
        super().__init__("dummy_endpoint_factory")
        self.endpoint_name = name
        self.task_handlers = task_handlers

    def get(self, parent: Node) -> Endpoint:
        return DummyEndpoint(self,
                             parent,
                             self.endpoint_name,
                             self.task_handlers)
