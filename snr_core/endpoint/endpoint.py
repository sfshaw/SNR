from snr_core.context.context import Context
from snr_core.endpoint.endpoint_factory import EndpointFactory
from snr_core.protocols import *
from snr_types import *


class Endpoint(Context, EndpointProtocol):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: NodeProtocol,
                 name: str,
                 ) -> None:
        super().__init__(name, parent)
        self.factory = factory
        self.parent = parent

    def reload(self, parent: NodeProtocol) -> EndpointProtocol:
        self.factory.reload()
        new_endpoint = self.factory.get(parent)
        return new_endpoint

    def __repr__(self) -> str:
        return self.name
