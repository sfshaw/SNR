from typing import Any, Callable, Optional, Tuple, TypeVar

from snr.type_defs import *
from typing_extensions import Protocol, runtime_checkable

ProfilingResult = Tuple[str, float]

T = TypeVar("T")


@runtime_checkable
class ProfilerProtocol(Protocol):
    settings: Settings

    def time(self,
             name: str,
             handler: Callable[..., T],
             *args: Any
             ) -> T:
        ...

    def dump(self) -> str:
        ...

    def is_alive(self) -> bool:
        ...

    def join_from(self, joiner: str) -> None:
        ...


ProfilerGetter = Callable[[],
                          Optional[ProfilerProtocol]]
