from typing import Any, Protocol


class Component(Protocol):
    name: str


class FactoryProtocol(Protocol):
    name: str

    def get(self, parent: Any) -> Component:
        raise NotImplementedError

    def reload(self) -> None:
        raise NotImplementedError

    def __repr__(self):
        return self.name
