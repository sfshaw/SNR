from snr.snr_protocol import *
from snr.snr_types import *


class Config(ConfigProtocol):
    def __init__(self,
                 mode: Mode,
                 factories: ComponentsByRole = {}
                 ) -> None:
        self.mode = mode
        self.factories = factories
        if not factories:
            raise Exception("No factories provided")

    def get(self, role: str) -> List[FactoryProtocol]:
        factories = self.factories[role]
        return factories
