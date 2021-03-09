from snr.protocol import *
from snr.type_defs import *

from ..contexts import Context
from .endpoint_factory import EndpointFactory


class Endpoint(Context, EndpointProtocol):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: NodeProtocol,
                 name: str,
                 ) -> None:
        super().__init__(name,
                         parent.settings,
                         parent.profiler,
                         parent.timer)
        self.factory = factory
        self.parent = parent

    def set_terminate_flag(self) -> None:
        pass

    def __repr__(self) -> str:
        return self.name
