import sys
from typing import List

from snr.config import MODE_DEBUG, MODE_DEPLOYED, Config
from snr.context import Context
from snr.factory import Factory
from snr.node import Node


class Runner():

    def __init__(self, mode: str, role: str, config: Config):
        self.mode = mode
        self.role = role
        self.factories = config.get(mode)[role]

    def run(self):
        raise NotImplementedError


def setup_node(context: Context,
               role: str,
               mode: str,
               factories: List[Factory]
               ) -> Node:
    py_v: str = sys.version[0:5]
    context.info("Starting {} node in {} mode using Python {}",
                 [role, mode, py_v])
    return Node(context, role, mode, factories)
