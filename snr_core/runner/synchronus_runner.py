from typing import Optional

from snr.config import Config, Role
from snr.node import Node
from snr.runner import Runner


class SynchronousRunner(Runner):

    def __init__(self, role: Role, config: Config):
        super().__init__(role, config)

    def run(self):
        with self.config.root_context("synchronous_runner") as context:
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
                    node.set_terminate_flag("Runner clean up")
                    node = None
