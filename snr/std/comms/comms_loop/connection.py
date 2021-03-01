from snr.types import *


@runtime_checkable
class Connection(Protocol):
    def is_closed(self) -> bool:
        ...

    def send(self, data: str):
        ...

    def poll(self, timeout_ms: float) -> bool:
        ...

    def recv(self) -> Any:
        ...

    def close(self) -> None:
        ...
