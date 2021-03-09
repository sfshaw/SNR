from snr.core import *
from snr.protocol import *
from snr.type_defs import *


class DummyEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: NodeProtocol,
                 name: str,
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
