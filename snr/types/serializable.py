from .base import *


@runtime_checkable
class Serializable(Protocol):
    def serialize(self) -> bytes:
        ...

    @classmethod
    def deserialize(cls, json: Optional[JsonData]) -> Optional["Serializable"]:
        ...
