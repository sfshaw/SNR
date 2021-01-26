from enum import Enum
from typing import Callable, Dict, List

from snr_core.context.root_context import RootContext
from snr_core.factory.factory_base import FactoryBase


class Mode(Enum):
    DEBUG = "debug"
    DEPLOYED = "deployed"
    TEST = "test"


Role = str
Components = List[FactoryBase]
ComponentsByRole = Dict[Role, Components]
ComponentsGetter = Callable[[str], ComponentsByRole]


class Config:
    def __init__(self,
                 mode: Mode,
                 factories: ComponentsByRole = {}
                 ) -> None:
        self.mode = mode
        self.factories = factories
        if not factories:
            raise Exception("No factories provided")

    def get(self, role: str) -> Components:
        return self.factories[role]

    def root_context(self,
                     name: str
                     ) -> RootContext:
        return RootContext(name)
