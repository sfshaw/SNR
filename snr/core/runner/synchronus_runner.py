from snr.protocol import *
from snr.types import *

from ..node import Node


class SynchronousRunner(RunnerProtocol):

    def __init__(self,
                 role: Role,
                 config: ConfigProtocol):
        self.role = role
        self.config = config

    def run(self) -> None:
        node: NodeProtocol = Node(self.role,
                                  self.config)
        try:
            node.loop()  # Blocking loop
        except KeyboardInterrupt:
            if node:
                print("Interrupted by user, exiting")
                node.set_terminate_flag("Interrupted by user")
            else:
                print("Exiting before node was done being constructed")
        finally:
            if node:
                if not node.is_terminated():
                    node.set_terminate_flag("Runner clean up")
