from typing import List

from snr.type_defs import *
from typing_extensions import Protocol, runtime_checkable

from .config_protocol import ConfigProtocol


@runtime_checkable
class MultiRunnerProtocol(Protocol):

    config: ConfigProtocol
    roles: List[Role]

    def run(self) -> None:
        ...
