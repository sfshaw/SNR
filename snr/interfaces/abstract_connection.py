from typing import Any, Optional

from snr.type_defs import *
from abc import ABC, abstractmethod


class AbstractConnection(ABC):
    @abstractmethod
    def open(self) -> None:
        ...

    @abstractmethod
    def is_closed(self) -> bool:
        ...

    @abstractmethod
    def send(self, data: bytes) -> None:
        ...

    @abstractmethod
    def poll(self, timeout_s: float) -> bool:
        ...

    @abstractmethod
    def recv(self) -> Optional[JsonData]:
        ...

    @abstractmethod
    def close(self) -> None:
        ...

    def __enter__(self) -> 'AbstractConnection':
        self.open()
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
