from abc import ABC, abstractmethod
from typing import List

from snr.type_defs import *

from .abstract_config import AbstractConfig


class AbstractMultiRunner(ABC):

    config: AbstractConfig
    roles: List[Role]

    @abstractmethod
    def run(self) -> None:
        ...
