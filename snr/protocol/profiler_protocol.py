from snr.types import *

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

    def dump(self) -> None:
        ...

    def join_from(self, joiner: str) -> None:
        ...
