from typing import List

from snr.type_defs import *
from typing_extensions import Protocol, runtime_checkable

from .abstract_config import AbstractConfig


@runtime_checkable
class AbstractMultiRunner(Protocol):

    config: AbstractConfig
    roles: List[Role]

    def run(self) -> None:
        ...
