
from threading import Thread
from typing import List

from snr.config import Config, Mode
from snr.root_context import RootContext
from snr.runner.multi_runner import MultiRunner
from snr.runner.runner import Runner
from snr.runner.synchronus_runner import SynchronousRunner
from snr.utils.utils import print_exit


class ThreadedRunner(MultiRunner):

    # TODO: Use a process since child thread cannot start other stuff

    def __init__(self, mode: Mode,  config: Config, roles: List[str]):
        factories_by_role = {}
        for role in roles:
            factories_by_role[role] = config.get(self.mode)[self.role]

        super().__init__(mode, config.get(mode))

    def run(self):
        context = RootContext("runner")
        runners: List[Runner] = [SynchronousRunner(
            self.mode,
            role,
            Config(factories={role: factories}))
            for (role, factories) in self.factories_by_role.items()]
        threads = [Thread(target=runner.run) for runner in runners]
        try:
            [thread.start() for thread in threads]
        except KeyboardInterrupt:
            print("TODO: Handle keyboard interrupt in runner threads")
            # for runner  in runners:
            #     if runner:
            #         context.log("framework", "Interrupted by user, exiting")
            #         node.set_terminate_flag("Interrupted by user")
            #     else:
            #         context.fatal(
            #             "Exiting before node was done being constructed")
        finally:
            for thread in threads:
                thread.join()

        context.terminate()
        print_exit("Ya done now")
