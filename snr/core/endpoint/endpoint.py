from snr.protocol import *
from snr.types import *

from ..context.context import Context
from .endpoint_factory import EndpointFactory


class Endpoint(Context, EndpointProtocol):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: NodeProtocol,
                 name: str,
                 ) -> None:
        super().__init__(name, parent.settings, parent.profiler)
        self.factory = factory
        self.parent = parent

    # def reload(self, parent: NodeProtocol) -> EndpointProtocol:
    #     self.factory.reload()
    #     new_endpoint = self.factory.get(parent)
    #     return new_endpoint

    def set_terminate_flag(self) -> None:
        pass

    def __repr__(self) -> str:
        return self.name
