import importlib
from typing import Optional

from snr_protocol.endpoint_protocol import EndpointProtocol
from snr_protocol.factory_protocol import FactoryProtocol
from snr_protocol.node_protocol import NodeProtocol


class EndpointFactory(FactoryProtocol):
    def __init__(self,
                 child_module: Optional[importlib.types.ModuleType],
                 name: str) -> None:
        self.name = name
        self.child_module = child_module

    def get(self, parent: NodeProtocol) -> EndpointProtocol:
        raise NotImplementedError

    def reload(self) -> None:
        if self.child_module:
            importlib.reload(self.child_module)
