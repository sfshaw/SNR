
from snr_core.loop.loop_protocol import LoopProtocol
from snr_core.factory.factory_protocol import FactoryProtocol
from snr_core.node import Node


class LoopFactory(FactoryProtocol):
    def __init__(self, name: str) -> None:
        self.name = name

    def get(self, parent: Node) -> LoopProtocol:
        raise NotImplementedError
