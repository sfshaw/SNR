from abc import ABC, abstractmethod
from typing import List

from .abstract_config import AbstractConfig
from .names import Role


class AbstractMultiRunner(ABC):

    config: AbstractConfig
    roles: List[Role]

    @abstractmethod
    def run(self) -> None:
        ...
