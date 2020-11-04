from snr.config import ComponentsByRole, Config, Mode
from snr.context import root_context
from snr.runner.runner import setup_node
from snr.runner.synchronus_runner import SynchronousRunner
from snr.runner.threaded_runner import ThreadedRunner


class TestRunner(ThreadedRunner):

    def __init__(self,
                 factories_by_role: ComponentsByRole
                 ) -> None:
        super(ThreadedRunner).__init__(Mode.DEBUG, factories_by_role)


class SynchronusTestRunner(SynchronousRunner):

    def __init__(self, config: Config) -> None:
        super().__init__(Mode.DEBUG, "test", config)

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
        print("Test Runner done")
