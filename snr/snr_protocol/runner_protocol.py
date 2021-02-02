from snr.snr_types import *

from .config_protocol import ConfigProtocol


@runtime_checkable
class RunnerProtocol(Protocol):
    role: Role
    config: ConfigProtocol

    def run(self) -> None:
        ...
