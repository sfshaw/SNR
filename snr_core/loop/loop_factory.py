
from snr_core.loop.loop_base import LoopBase
from snr_core.factory.factory_base import FactoryBase
from snr_core.node import Node


class LoopFactory(FactoryBase):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def get(self, parent: Node) -> LoopBase:
        raise NotImplementedError
