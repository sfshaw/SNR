from snr.types import *


@runtime_checkable
class ConnectionProtocol(Protocol):

    def open(self) -> None:
        ...

    def is_closed(self) -> bool:
        ...

    def send(self, data: bytes) -> None:
        ...

    def poll(self, timeout_s: float) -> bool:
        ...

    def recv(self) -> Optional[JsonData]:
        ...

    def close(self) -> None:
        ...

    def __enter__(self) -> 'ConnectionProtocol':
        self.open()
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
