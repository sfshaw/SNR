'''Provides concrete implementation of AbstractConfig by wrapping mode and a
 dictionary of factories by role.
A single Config contains the information to construct all the nodes used by
system or robot. With one Config definition, the components of multiple nodes
can be defined in one place.
'''

from typing import List, Optional

from snr.interfaces import *
from snr.type_defs import *

from ..core.contexts import local_profiler


class Config(AbstractConfig):

    factories: ComponentsByRole

    def __init__(self,
                 mode: Mode = Mode.DEPLOYED,
                 factories: ComponentsByRole = {},
                 ) -> None:
        self.mode = mode
        self.factories = factories
        if not factories:
            raise Exception("No factories provided")

    def get(self, role: str) -> List[AbstractFactory]:
        factories = self.factories[role]
        return factories

    def get_profiler(self) -> Optional[AbstractProfiler]:
        if self.mode in [Mode.DEBUG]:
            return local_profiler.LocalProfiler()
        return None
