from enum import Enum
from typing import Callable, Dict, List, Optional

from snr_core.context.root_context import RootContext
from snr_core.context.silent_stdout import SilentStdOut
from snr_core.context.stdout import StdOut
from snr_core.context.stdout_consumer import StdOutConsumer
from snr_core.factory.factory_base import FactoryBase

Role = str


class Mode(Enum):
    DEBUG = "debug"
    DEPLOYED = "deployed"
    TEST = "test"


Components = List[FactoryBase]
ComponentsByRole = Dict[Role, Components]
ComponentsGetter = Callable[[str], ComponentsByRole]


class Config:
    def __init__(self,
                 mode: Mode,
                 factories: ComponentsByRole = {},
                 stdout: Optional[StdOutConsumer] = None
                 ) -> None:
        self.mode = mode
        self.factories = factories
        self.stdout = stdout
        if not factories:
            raise Exception("No factories provided")

    def get(self, role: str) -> Components:
        return self.factories[role]

    def root_context(self,
                     name: str
                     ) -> RootContext:
        if not self.stdout:
            self.stdout = {
                Mode.DEPLOYED: StdOut,
                Mode.DEBUG: StdOut,
                Mode.TEST: SilentStdOut,
            }[self.mode](name)
        return RootContext(name, self.stdout)
