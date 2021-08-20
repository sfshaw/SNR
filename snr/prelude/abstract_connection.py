from abc import ABC, abstractmethod
from typing import Any, Optional

from .serializable import JsonData


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
