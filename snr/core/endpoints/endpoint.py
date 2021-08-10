from snr.interfaces import *
from snr.type_defs import *

from ..contexts import Context
from .endpoint_factory import EndpointFactory


class Endpoint(Context, AbstractEndpoint):

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

    def task_source(self) -> SomeTasks:
        return None

    def set_terminate_flag(self) -> None:
        pass

    def __repr__(self) -> str:
        return self.name
