from .base import *


@runtime_checkable
class Serializable(Protocol):
    def serialize(self) -> JsonData:
        ...

    @classmethod
    def deserialize(cls, json: JsonData) -> Optional["Serializable"]:
        ...
