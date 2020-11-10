from snr.config import Config, Mode, Role
from snr.node import Node
from snr.root_context import RootContext
from snr.runner.runner import Runner
from snr.utils.utils import print_exit


class SynchronousRunner(Runner):

    def __init__(self, mode: Mode, role: Role, config: Config):
        super().__init__(mode, role, config)

    def run(self):
        context = RootContext("runner")
        node = None
        try:
            node = Node(context, self.role, self.mode, self.factories)
            node.loop()  # Blocking loop
        except KeyboardInterrupt:
            if node:
                print("Interrupted by user, exiting")
                node.set_terminate_flag("Interrupted by user")
            else:
                print("Exiting before node was done being constructed")
        finally:
            if node:
                node.terminate()
                node = None
        context.terminate()
        print_exit("Ya done now")
