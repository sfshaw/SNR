from snr_types import *

from snr_core.protocols import *


class Config(ConfigProtocol):
    def __init__(self,
                 mode: Mode,
                 factories: ComponentsByRole = {}
                 ) -> None:
        self.mode = mode
        self.factories = factories
        if not factories:
            raise Exception("No factories provided")

    def get(self, role: str) -> Components:
        factories = self.factories[role]
        return factories
