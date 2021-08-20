from typing import List

from snr.prelude import *

from ..contexts import Context
from .endpoint_factory import EndpointFactory


class Endpoint(Context, AbstractEndpoint):

    factory: EndpointFactory
    parent: AbstractNode
    task_handlers: TaskHandlerMap

    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 name: ComponentName,
                 ) -> None:
        super().__init__(name,
                         parent.profiler,
                         parent.timer)
        self.factory = factory
        self.parent = parent

    def task_source(self) -> List[Task]:
        return []

    def set_terminate_flag(self) -> None:
        pass

    def __repr__(self) -> ComponentName:
        return self.name
