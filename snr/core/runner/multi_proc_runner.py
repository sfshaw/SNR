import multiprocessing as mp
from typing import List

from snr.protocol import *
from snr.type_defs import *

from ..node import Node


class MultiProcRunner(MultiRunnerProtocol):

    def __init__(self,
                 config: ConfigProtocol,
                 roles: List[str],
                 ) -> None:
        self.roles = roles
        self.mode = config.mode
        self.config = config

    def run(self):
        nodes: List[NodeProtocol] = [Node(role,
                                          self.config)
                                     for role in self.roles]

        def run_node(node: NodeProtocol) -> None:
            node.loop()

        processes = [mp.Process(target=run_node,
                                name=node.name + "_proc",
                                args=(node,))
                     for node in nodes]

        try:
            for proc in processes:
                proc.start()
            terminate: bool = False
            while not terminate:
                terminate = all([node.is_terminated() for node in nodes])
        except KeyboardInterrupt:
            print("TODO: Handle keyboard interrupt in runner processes")
            # for runner  in runners:
            #     if runner:
            #        context.log("framework", "Interrupted by user, exiting")
            #         node.set_terminate_flag("Interrupted by user")
            #     else:
            #         context.fatal(
            #             "Exiting before node was done being constructed")
        finally:
            for node in nodes:
                if node:
                    if not node.is_terminated():
                        node.set_terminate_flag("Runner clean up")
            for proc in processes:
                proc.join()
