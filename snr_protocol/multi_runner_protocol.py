from typing import List, Protocol

from snr_types import *

from snr_protocol.factory_protocol import ComponentsByRole


class MultiRunner(Protocol):

    mode: Mode
    factories_by_role: ComponentsByRole

    def run(self, roles: List[Role]) -> None:
        ...
