from snr.types import *


@runtime_checkable
class ComponentProtocol(Protocol):
    name: str

    def start(self) -> None:
        ...

    def join(self) -> None:
        ...
