from typing import Protocol

from snr_types import *

from snr_protocol.factory_protocol import Components


class ConfigProtocol(Protocol):
    mode: Mode

    def get(self, role: str) -> Components:
        ...
