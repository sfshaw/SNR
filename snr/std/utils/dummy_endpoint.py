from snr.core.base import *

DEFAULT_NAME = "dummy_endpoint"


class DummyEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: NodeProtocol,
                 name: str = DEFAULT_NAME,
                 task_handlers: TaskHandlerMap = {},
                 ) -> None:
        super().__init__(factory,
                         parent,
                         name)
        self.task_handlers = task_handlers

    def task_source(self) -> None:
        return None

    def start(self) -> None:
        pass

    def terminate(self) -> None:
        pass


class DummyEndpointFactory(EndpointFactory):
    def __init__(self,
                 name: str = DEFAULT_NAME,
                 task_handlers: TaskHandlerMap = {}
                 ) -> None:
        super().__init__()
        self.endpoint_name = name
        self.task_handlers = task_handlers

    def get(self, parent: NodeProtocol) -> EndpointProtocol:
        return DummyEndpoint(self,
                             parent,
                             self.endpoint_name,
                             self.task_handlers)
