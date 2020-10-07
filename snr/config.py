from typing import Callable, Dict, List

from snr.factory import Factory

MODE_DEBUG: str = "debug"
MODE_DEPLOYED: str = "deployed"


class Config:
    def __init__(self,
                 components_by_role: Dict[str, List[Factory]] = None,
                 get_components: Callable[[str], List[Factory]] = None
                 ):
        self.components = components_by_role
        self.get_components = get_components
        if (self.components is None) and (self.get_components is None):
            raise Exception("No componets provided")

    def get(self, mode: str) -> Dict[str, List[Factory]]:
        if self.get_components:
            return self.get_components(mode)
        return self.components
