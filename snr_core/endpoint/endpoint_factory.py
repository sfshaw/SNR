import importlib
from typing import Optional

from snr_core.endpoint.endpoint_protocol import EndpointProtocol
from snr_core.factory.factory_protocol import FactoryProtocol
from snr_core.node import Node


class EndpointFactory(FactoryProtocol):
    def __init__(self,
                 child_module: Optional[importlib.types.ModuleType],
                 name: str) -> None:
        self.name = name
        self.child_module = child_module

    def get(self, parent: Node) -> EndpointProtocol:
        raise NotImplementedError

    def reload(self) -> None:
        if self.child_module:
            importlib.reload(self.child_module)
