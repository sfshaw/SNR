import importlib
from types import ModuleType
from typing import Optional

from snr.snr_protocol.endpoint_protocol import EndpointProtocol
from snr.snr_protocol.factory_protocol import FactoryProtocol
from snr.snr_protocol.node_protocol import NodeProtocol
from snr.snr_types import *


class EndpointFactory(FactoryProtocol):
    def __init__(self,
                 child_module: Optional[ModuleType],
                 name: str) -> None:
        self.name = name
        self.child_module = child_module

    def get(self, parent: NodeProtocol) -> EndpointProtocol:
        raise NotImplementedError

    def reload(self) -> None:
        if self.child_module:
            importlib.reload(self.child_module)
