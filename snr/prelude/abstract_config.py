from abc import ABC, abstractmethod
from typing import Any, List, Optional

from .mode import Mode

from .abstract_factory import AbstractFactory
from .abstract_profiler import AbstractProfiler


class AbstractConfig(ABC):

    mode: Mode

    @abstractmethod
    def get(self, role: str) -> List[AbstractFactory[Any]]:
        ...

    @abstractmethod
    def get_profiler(self) -> Optional[AbstractProfiler]:
        ...
