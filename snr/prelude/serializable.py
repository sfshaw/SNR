from typing import Optional, Union

from typing_extensions import Protocol, runtime_checkable

JsonData = Union[str, bytes, bytearray]


@runtime_checkable
class Serializable(Protocol):
    def serialize(self) -> bytes:
        ...

    @classmethod
    def deserialize(cls,
                    json: Optional[JsonData],
                    ) -> Optional["Serializable"]:
        ...
