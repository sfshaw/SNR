from typing import List

from snr.snr_types import *

from snr.snr_protocol.factory_protocol import ComponentsByRole


@runtime_checkable
class MultiRunner(Protocol):

    mode: Mode
    factories_by_role: ComponentsByRole

    def run(self, roles: List[Role]) -> None:
        ...
