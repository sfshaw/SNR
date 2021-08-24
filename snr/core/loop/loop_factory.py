from abc import abstractmethod
from snr.prelude import *
from types import ModuleType


class LoopFactory(AbstractFactory[AbstractLoop]):
    def __init__(self,
                 reload_targets: ReloadTargets = [],
                 ) -> None:
        if isinstance(reload_targets, ModuleType):
            reload_targets = [reload_targets]
        self.reload_targets = reload_targets

    @abstractmethod
    def get(self, parent: AbstractNode) -> AbstractLoop:
        ...
