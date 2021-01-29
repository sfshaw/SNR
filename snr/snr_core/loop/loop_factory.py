import importlib
from types import ModuleType

from snr.snr_protocol.factory_protocol import FactoryProtocol
from snr.snr_protocol.loop_protocol import LoopProtocol
from snr.snr_protocol.node_protocol import NodeProtocol
from snr.snr_types import *


class LoopFactory(FactoryProtocol):
    def __init__(self,
                 name: str,
                 child_module: Optional[ModuleType] = None) -> None:
        self.name = name
        self.child_module = child_module

    def get(self, parent: NodeProtocol) -> LoopProtocol:
        raise NotImplementedError

    def reload(self) -> None:
        if self.child_module:
            importlib.reload(self.child_module)
