from .base import *


@runtime_checkable
class Serializable(Protocol):
    def serialize(self) -> str:
        ...

    @classmethod
    def deserialize(cls, json: str) -> Optional["Serializable"]:
        ...
