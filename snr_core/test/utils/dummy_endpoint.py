from snr_core.base import *

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
                         name,
                         task_handlers=task_handlers)

    def start(self) -> None:
        pass

    def terminate(self) -> None:
        pass


class DummyEndpointFactory(EndpointFactory):
    def __init__(self,
                 name: str = DEFAULT_NAME,
                 task_handlers: TaskHandlerMap = {}
                 ) -> None:
        super().__init__(None, "dummy_endpoint_factory")
        self.endpoint_name = name
        self.task_handlers = task_handlers

    def get(self, parent: NodeProtocol) -> EndpointProtocol:
        return DummyEndpoint(self,
                             parent,
                             self.endpoint_name,
                             self.task_handlers)
