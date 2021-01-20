from snr_core.endpoint.endpoint import Endpoint, EndpointBase
from snr_core.endpoint.endpoint_factory import EndpointFactory
from snr_core.node import Node
from snr_core.task import TaskHandlerMap

DEFAULT_NAME = "dummy_endpoint"


class DummyEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: Node,
                 name: str = DEFAULT_NAME,
                 task_handlers: TaskHandlerMap = {},
                 ) -> None:
        super().__init__(factory,
                         parent,
                         name,
                         task_handlers=task_handlers)


class DummyEndpointFactory(EndpointFactory):
    def __init__(self,
                 name: str = DEFAULT_NAME,
                 task_handlers: TaskHandlerMap = {}
                 ) -> None:
        super().__init__("dummy_endpoint_factory")
        self.endpoint_name = name
        self.task_handlers = task_handlers

    def get(self, parent: Node) -> EndpointBase:
        return DummyEndpoint(self,
                             parent,
                             self.endpoint_name,
                             self.task_handlers)
