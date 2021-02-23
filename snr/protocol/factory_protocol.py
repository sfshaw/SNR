import importlib

from snr.types import *

from .component_protocol import ComponentProtocol


@runtime_checkable
class FactoryProtocol(Protocol):
    child_module: Optional[ModuleType]

    def get(self, parent: Any) -> ComponentProtocol:
        raise NotImplementedError

    def reload(self) -> None:
        if self.child_module:
            importlib.reload(self.child_module)

    def __repr__(self):
        return self.__class__.__name__


ComponentsByRole = Dict[Role, List[FactoryProtocol]]
