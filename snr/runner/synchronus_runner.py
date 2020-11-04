from snr.config import Config
from snr.context import root_context
from snr.runner.runner import Runner, setup_node
from snr.utils.utils import print_exit


class SynchronousRunner(Runner):

    def __init__(self, mode: str, role: str, config: Config):
        super().__init__(mode, role, config)

    def run(self):
        context = root_context("runner")
        node = None
        try:
            node = setup_node(context, self.role, self.mode, self.factories)
            node.loop()  # Blocking loop
        except KeyboardInterrupt:
            if node:
                context.log("Interrupted by user, exiting")
                node.set_terminate_flag("Interrupted by user")
            else:
                context.fatal("Exiting before node was done being constructed")
        finally:
            if node:
                node.terminate()
                node = None
        context.terminate()
        print_exit("Ya done now")
