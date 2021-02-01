from snr.snr_types import *

ProfilingResult = Tuple[str, float]


@runtime_checkable
class ProfilerProtocol(Protocol):
    settings: Settings

    def time(self,
             name: str,
             handler: Callable[..., Any],
             args: List[Any]
             ) -> Any:
        ...

    def dump(self) -> None:
        ...

    def join_from(self, joiner: str) -> None:
        ...
