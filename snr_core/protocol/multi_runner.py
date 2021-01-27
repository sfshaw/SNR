from typing import List, Protocol

from snr_core.config import Mode
from snr_core.modes import ComponentsByRole, Role


class MultiRunner(Protocol):

    mode: Mode
    factories_by_role: ComponentsByRole

    def run(self, roles: List[Role]) -> None:
        ...
