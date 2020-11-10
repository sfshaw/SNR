
from typing import Any

from snr.config import Config, Mode, Role


class Runner():

    def __init__(self, mode: Mode, role: Role, config: Config):
        self.mode = mode
        self.role = role
        self.factories = config.get(mode)[role]

    def run(self) -> Any:
        raise NotImplementedError
