from typing import Protocol


class FactoryProtocol(Protocol):

    def reload(self) -> None:
        ...
