from snr.snr_protocol import *

from snr.snr_core.config import Config
from snr.snr_core.context.root_context import RootContext
from snr.snr_core.node import Node


class SynchronousRunner(RunnerProtocol):

    def __init__(self, role: Role, config: Config):
        self.role = role
        self.config = config

    def run(self) -> None:
        context = RootContext("synchronous_runner")
        components = self.config.get(self.role)
        node: NodeProtocol = Node(context,
                                  self.role,
                                  self.config.mode,
                                  components)
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
                if not node.is_terminated.is_set():
                    node.set_terminate_flag("Runner clean up")
