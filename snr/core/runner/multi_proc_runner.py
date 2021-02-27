import logging
import multiprocessing as mp

from snr.protocol import *
from snr.types import *

from ..context.root_context import RootContext
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
        context = RootContext("runner")
        context.log.setLevel(logging.WARN)
        nodes: List[NodeProtocol] = [
            Node(context,
                 role,
                 self.mode,
                 self.config.get(role))
            for role in self.roles]
        processes = [mp.Process(
            target=node.loop) for node in nodes]
        try:
            for proc in processes:
                proc.start()
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
