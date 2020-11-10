from snr.config import ComponentsByRole, Config, Mode
from snr.node import Node
from snr.root_context import RootContext
from snr.runner.synchronus_runner import SynchronousRunner
from snr.runner.threaded_runner import ThreadedRunner


class TestRunner(ThreadedRunner):

    def __init__(self,
                 factories_by_role: ComponentsByRole
                 ) -> None:
        super(ThreadedRunner).__init__(Mode.DEBUG, factories_by_role)


class SynchronusTestRunnerStartupOnly(SynchronousRunner):

    def __init__(self, config: Config) -> None:
        super().__init__(Mode.DEBUG, "test", config)

    def run(self):
        context = RootContext("runner")
        node = None
        try:
            node = Node(context, self.role, self.mode, self.factories)
            node.terminate()
        except KeyboardInterrupt:
            if node:
                print("Interrupted by user, exiting")
                node.set_terminate_flag("Interrupted by user")
            else:
                print("Exiting before node was done being constructed")
        finally:
            if node:
                node = None
        context.terminate()
        print("Test Runner done")


class SynchronusTestRunner(SynchronousRunner):

    def __init__(self, config: Config) -> None:
        super().__init__(Mode.DEBUG, "test", config)

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
        print("Test Runner done")
