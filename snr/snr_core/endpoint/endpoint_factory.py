import importlib

from snr.snr_protocol import *


class EndpointFactory(FactoryProtocol):
    def __init__(self,
                 child_module: Optional[ModuleType] = None,
                 ) -> None:
        self.child_module = child_module

    def reload(self) -> None:
        if self.child_module:
            importlib.reload(self.child_module)
