import sys
from typing import Any, List

from snr.config import Config, Mode, Role
from snr.context import Context
from snr.factory import Factory
from snr.node import Node


class Runner():

    def __init__(self, mode: Mode, role: Role, config: Config):
        self.mode = mode
        self.role = role
        self.factories = config.get(mode)[role]

    def run(self) -> Any:
        raise NotImplementedError


def setup_node(context: Context,
               role: Role,
               mode: Mode,
               factories: List[Factory]
               ) -> Node:
    py_v: str = sys.version[0:5]
    context.info("Starting {} node in {} mode using Python {}",
                 [role, mode, py_v])
    return Node(context, role, mode, factories)
