from types import ModuleType

from snr.protocol import *
from snr.type_defs import *


class EndpointFactory(FactoryProtocol):
    def __init__(self,
                 reload_targets: ReloadTargets = [],
                 ) -> None:
        if isinstance(reload_targets, ModuleType):
            reload_targets = [reload_targets]
        self.reload_targets = reload_targets
