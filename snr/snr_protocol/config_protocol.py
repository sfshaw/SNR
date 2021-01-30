from typing import List

from snr.snr_types import *

from .factory_protocol import FactoryProtocol


@runtime_checkable
class ConfigProtocol(Protocol):
    mode: Mode

    def get(self, role: str) -> List[FactoryProtocol]:
        ...
