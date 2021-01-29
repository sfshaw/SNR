from typing import Optional

from snr.snr_core.config import Config
from snr.snr_core.context.root_context import RootContext
from snr.snr_core.datastore import Datastore
from snr.snr_core.endpoint.node_core_factory import NodeCoreFactory
from snr.snr_core.node import Node
from snr.snr_protocol import *
from snr.snr_protocol.node_protocol import NodeProtocol
from snr.snr_types import *


class SynchronousRunner(RunnerProtocol):

    def __init__(self, role: Role, config: Config):
        self.role = role
        self.config = config

    def run(self) -> None:
        context = RootContext("synchronous_runner")
        node: Optional[NodeProtocol] = None
        try:
            components = self.config.get(self.role)
            components.append(NodeCoreFactory())
            node = Node(context,
                        self.role,
                        self.config.mode,
                        components,
                        lambda n, s: Datastore(n, s))
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
