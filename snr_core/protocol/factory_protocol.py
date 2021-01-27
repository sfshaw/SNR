from typing import Any, Protocol

from snr_core.protocol.component_protocol import Component


class FactoryProtocol(Protocol):
    name: str

    def get(self, parent: Any) -> Component:
        raise NotImplementedError

    def reload(self) -> None:
        raise NotImplementedError

    def __repr__(self):
        return self.name
