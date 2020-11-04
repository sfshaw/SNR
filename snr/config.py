from typing import Callable, Dict, List, Optional

from snr.factory import Factory

MODE_DEBUG: str = "debug"
MODE_DEPLOYED: str = "deployed"

ComponentsByRole = Dict[str, List[Factory]]
ComponentsGetter = Callable[[str], ComponentsByRole]


# def get_empty(role: str) -> ComponentsByRole:
#     empty: ComponentsByRole = {}
#     return empty


class Config:
    def __init__(self,
                 factories: ComponentsByRole = {},
                 get_factories: Optional[ComponentsGetter] = None
                 ):
        self.factories = factories
        self.get_factories = get_factories
        if (not self.factories) and (not self.get_factories):
            raise Exception("No componets provided")

    def get(self, mode: str) -> ComponentsByRole:
        if self.get_factories:
            self.factories = self.get_factories(mode)
        return self.factories
