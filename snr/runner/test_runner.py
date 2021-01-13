
from snr.config import Config
from snr.runner.synchronus_runner import SynchronousRunner

# class TestRunner(ThreadedRunner):

#     def __init__(self,
#                  factories_by_role: ComponentsByRole
#                  ) -> None:
#         super(ThreadedRunner).__init__(Mode.DEBUG, factories_by_role)


# class SynchronusTestRunnerStartupOnly(Runner):

#     def __init__(self, config: Config) -> None:
#         super().__init__(Mode.DEBUG, "test", config)

#     def run(self):
#         with RootContext("runner") as context:
#             node: Optional[Node] = None
#             try:
#                 node = Node(context, self.role, self.mode, self.factories)
#                 node.set_terminate_flag("test complete")
#             except KeyboardInterrupt:
#                 if node:
#                     print("Interrupted by user, exiting")
#                     node.set_terminate_flag("Interrupted by user")
#                 else:
#                     print("Exiting before node was done being constructed")
#             finally:
#                 if node:
#                     node = None
#         print("Test Runner done")


class SynchronusTestRunner(SynchronousRunner):

    def __init__(self,
                 config: Config
                 ) -> None:
        super().__init__("test", config)
