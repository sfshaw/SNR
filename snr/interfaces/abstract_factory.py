import importlib
from abc import ABC, abstractmethod
from types import ModuleType
from typing import Any, Dict, List

from snr.type_defs import *


class AbstractFactory(ABC):
    reload_targets: List[ModuleType]

    @abstractmethod
    def get(self, parent: Any) -> Any:
        ...

    def reload(self) -> None:
        for module in self.reload_targets:
            importlib.reload(module)

    def __repr__(self):
        return self.__class__.__name__


ComponentsByRole = Dict[Role, List[AbstractFactory]]
