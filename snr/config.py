from enum import Enum
from typing import Callable, Dict, List, Optional

from snr.factory import Factory

Role = str


class Mode(Enum):
    DEBUG = "debug"
    DEPLOYED = "deployed"
    TEST = "test"


ComponentsByRole = Dict[Role, List[Factory]]
ComponentsGetter = Callable[[Mode], ComponentsByRole]


class Config:
    def __init__(self,
                 factories: ComponentsByRole = {},
                 get_factories: Optional[ComponentsGetter] = None
                 ):
        self.factories = factories
        self.get_factories = get_factories
        if (not self.factories) and (not self.get_factories):
            raise Exception("No componets provided")

    def get(self, mode: Mode) -> ComponentsByRole:
        if self.get_factories:
            self.factories = self.get_factories(mode)
        return self.factories
