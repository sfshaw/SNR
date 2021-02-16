import multiprocessing

from snr.snr_protocol import *
from snr.snr_types import *

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
        nodes: List[NodeProtocol] = [
            Node(context,
                 role,
                 self.mode,
                 self.config.get(role))
            for role in self.roles]
        procs = [multiprocessing.Process(
            target=node.loop) for node in nodes]
        try:
            [thread.start() for thread in procs]
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
            for thread in procs:
                thread.join()
