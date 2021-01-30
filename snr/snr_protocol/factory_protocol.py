from typing import Any, Callable, Dict, List

from snr.snr_types import *

from snr.snr_protocol.component_protocol import ComponentProtocol


@runtime_checkable
class FactoryProtocol(Protocol):
    name: str

    def get(self, parent: Any) -> ComponentProtocol:
        raise NotImplementedError

    def reload(self) -> None:
        raise NotImplementedError

    def __repr__(self):
        return self.name


ComponentsByRole = Dict[Role, List[FactoryProtocol]]
