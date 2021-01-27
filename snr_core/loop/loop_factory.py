from snr_core.protocol.factory_protocol import FactoryProtocol
from snr_core.protocol.loop_protocol import LoopProtocol
from snr_core.protocol.node_protocol import NodeProtocol


class LoopFactory(FactoryProtocol):
    def __init__(self, name: str) -> None:
        self.name = name

    def get(self, parent: NodeProtocol) -> LoopProtocol:
        raise NotImplementedError
