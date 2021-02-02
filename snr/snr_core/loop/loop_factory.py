from snr.snr_protocol import *
from snr.snr_types import *


class LoopFactory(FactoryProtocol):
    def __init__(self,
                 child_module: Optional[ModuleType] = None
                 ) -> None:
        self.child_module = child_module
