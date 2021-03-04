from snr.types import *


@runtime_checkable
class Connection(Protocol):

    def open(self) -> None:
        ...

    def is_closed(self) -> bool:
        ...

    def send(self, data: JsonData):
        ...

    def poll(self, timeout_ms: float) -> bool:
        ...

    def recv(self) -> Optional[JsonData]:
        ...

    def close(self) -> None:
        ...
