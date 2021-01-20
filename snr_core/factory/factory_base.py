from typing import Any, Union

from snr_core.endpoint.endpoint_base import EndpointBase
from snr_core.loop.loop_base import LoopBase

Component = Union[EndpointBase, LoopBase]


class FactoryBase:
    def __init__(self, name: str) -> None:
        self.name = name

    def get(self, parent: Any) -> Component:
        raise NotImplementedError

    def reload(self) -> None:
        raise NotImplementedError

    def __repr__(self):
        return self.name
