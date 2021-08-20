from typing import List

from snr.core import *
from snr.prelude import *


class DummyEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 name: str,
                 task_handlers: TaskHandlerMap = {},
                 ) -> None:
        super().__init__(factory,
                         parent,
                         name)
        self.task_handlers = task_handlers

    def task_source(self) -> List[Task]:
        return []

    def begin(self) -> None:
        pass

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass
