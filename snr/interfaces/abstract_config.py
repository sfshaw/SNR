from abc import ABC, abstractmethod
from typing import List, Optional

from snr.type_defs import *

from .abstract_factory import AbstractFactory
from .abstract_profiler import AbstractProfiler


class AbstractConfig(ABC):
    mode: Mode
    settings: Settings

    @abstractmethod
    def get(self, role: str) -> List[AbstractFactory]:
        ...

    @abstractmethod
    def get_profiler(self) -> Optional[AbstractProfiler]:
        ...
