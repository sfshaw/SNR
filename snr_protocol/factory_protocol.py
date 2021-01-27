from typing import Any, Callable, Dict, List, Protocol

from snr_types.role import Role

from snr_protocol.component_protocol import ComponentProtocol


class FactoryProtocol(Protocol):
    name: str

    def get(self, parent: Any) -> ComponentProtocol:
        raise NotImplementedError

    def reload(self) -> None:
        raise NotImplementedError

    def __repr__(self):
        return self.name


Components = List[FactoryProtocol]
ComponentsByRole = Dict[Role, Components]
ComponentsGetter = Callable[[Role], ComponentsByRole]
