'''Provides concrete implementation of ConfigProtocol by wrapping mode and a
 dictionary of factories by role.
A single Config contains the information to construct all the nodes used by
system or robot. With one Config definition, the components of multiple nodes
can be defined in one place.
'''

from typing import List, Optional

from snr.protocol import *
from snr.type_defs import *

from ..core.utils.profiler import Profiler


class Config(ConfigProtocol):
    def __init__(self,
                 mode: Mode = Mode.DEPLOYED,
                 factories: ComponentsByRole = {},
                 ) -> None:
        self.mode = mode
        self.factories = factories
        self.settings = Settings()
        if not factories:
            raise Exception("No factories provided")

    def get(self, role: str) -> List[FactoryProtocol]:
        factories = self.factories[role]
        return factories

    def get_profiler(self) -> Optional[ProfilerProtocol]:
        if self.mode in [Mode.DEBUG]:
            return Profiler(self.settings)
        return None
