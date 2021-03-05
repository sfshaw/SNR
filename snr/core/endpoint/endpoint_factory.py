from snr.protocol import *
from snr.types import *


class EndpointFactory(FactoryProtocol):
    def __init__(self,
                 reload_targets: Union[ModuleType,
                                       List[ModuleType]] = [],
                 ) -> None:
        if isinstance(reload_targets, ModuleType):
            reload_targets = [reload_targets]
        self.reload_targets = reload_targets
