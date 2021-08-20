from abc import ABC, abstractmethod
from types import ModuleType

from snr.prelude import *


class EndpointFactory(AbstractFactory[AbstractEndpoint], ABC):
    def __init__(self,
                 reload_targets: ReloadTargets = [],
                 ) -> None:
        if isinstance(reload_targets, ModuleType):
            reload_targets = [reload_targets]
        self.reload_targets = reload_targets

    @abstractmethod
    def get(self, parent: AbstractNode) -> AbstractEndpoint:
        ...
