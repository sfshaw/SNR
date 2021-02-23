from snr.types import *

from .config_protocol import ConfigProtocol


@runtime_checkable
class MultiRunnerProtocol(Protocol):

    config: ConfigProtocol
    roles: List[Role]

    def run(self) -> None:
        ...
