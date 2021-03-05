import importlib

from snr.types import *

from .component_protocol import ComponentProtocol


@runtime_checkable
class FactoryProtocol(Protocol):
    reload_targets: List[ModuleType]

    def get(self, parent: Any) -> ComponentProtocol:
        raise NotImplementedError

    def reload(self) -> None:
        for module in self.reload_targets:
            importlib.reload(module)

    def __repr__(self):
        return self.__class__.__name__


ComponentsByRole = Dict[Role, List[FactoryProtocol]]
