from snr.snr_types import *

from snr.snr_protocol.factory_protocol import Components


@runtime_checkable
class ConfigProtocol(Protocol):
    mode: Mode

    def get(self, role: str) -> Components:
        ...
