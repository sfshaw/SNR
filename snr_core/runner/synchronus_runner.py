from typing import Optional

from snr_core.config import Config
from snr_core.modes import Role
from snr_core.node import Node


class SynchronousRunner:

    def __init__(self, role: Role, config: Config):
        self.role = role
        self.config = config

    def run(self) -> None:
        context = self.config.root_context("synchronous_runner")
        node: Optional[Node] = None
        try:
            node = Node(context,
                        self.role,
                        self.config.mode,
                        self.config.get(self.role))
            node.loop()  # Blocking loop
        except KeyboardInterrupt:
            if node:
                print("Interrupted by user, exiting")
                node.set_terminate_flag("Interrupted by user")
            else:
                print("Exiting before node was done being constructed")
        finally:
            if node:
                if not node.is_terminated.is_set():
                    node.set_terminate_flag("Runner clean up")
