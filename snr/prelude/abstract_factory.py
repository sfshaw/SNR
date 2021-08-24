import importlib
from abc import ABC, abstractmethod
from types import ModuleType
from typing import Any, Dict, Generic, List, TypeVar

from .names import Role

T = TypeVar('T')


class AbstractFactory(ABC, Generic[T]):
    reload_targets: List[ModuleType]

    @abstractmethod
    def get(self, parent: Any) -> T:
        ...

    def reload(self) -> None:
        for module in self.reload_targets:
            importlib.reload(module)

    def __repr__(self):
        return self.__class__.__name__


ComponentsByRole = Dict[Role, List[AbstractFactory[Any]]]
