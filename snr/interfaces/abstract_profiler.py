from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Tuple, TypeVar

from snr.type_defs import *

ProfilingResult = Tuple[str, float]

T = TypeVar("T")


class AbstractProfiler(ABC):
    settings: Settings

    @abstractmethod
    def time(self,
             name: str,
             handler: Callable[..., T],
             *args: Any
             ) -> T:
        ...

    @abstractmethod
    def dump(self) -> str:
        ...

    @abstractmethod
    def is_alive(self) -> bool:
        ...

    @abstractmethod
    def join_from(self, joiner: str) -> None:
        ...


ProfilerGetter = Callable[[],
                          Optional[AbstractProfiler]]
