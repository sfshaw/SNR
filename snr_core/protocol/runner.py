
from typing import Protocol

from snr_core.config import Config
from snr_core.modes import Role


class Runner(Protocol):
    role: Role
    config: Config

    def run(self) -> None:
        ...
