import importlib
from types import ModuleType
from typing import Any, Dict, List

from snr.type_defs import *
from typing_extensions import Protocol, runtime_checkable

from .component_protocol import ComponentProtocol


@runtime_checkable
class FactoryProtocol(Protocol):
    reload_targets: List[ModuleType]

    def get(self, parent: Any) -> ComponentProtocol:
        ...

    def reload(self) -> None:
        for module in self.reload_targets:
            importlib.reload(module)

    def __repr__(self):
        return self.__class__.__name__


ComponentsByRole = Dict[Role, List[FactoryProtocol]]
