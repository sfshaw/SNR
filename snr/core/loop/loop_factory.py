from snr.protocol import *
from snr.type_defs import *
from types import ModuleType


class LoopFactory(FactoryProtocol):
    def __init__(self,
                 reload_targets: ReloadTargets = [],
                 ) -> None:
        if isinstance(reload_targets, ModuleType):
            reload_targets = [reload_targets]
        self.reload_targets = reload_targets
