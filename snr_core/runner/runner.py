
from typing import Any

from snr_core.config import Config, Role


class Runner():

    def __init__(self,
                 role: Role,
                 config: Config) -> None:
        self.role = role
        self.config = config

    def run(self) -> Any:
        raise NotImplementedError
