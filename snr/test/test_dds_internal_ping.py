from time import time

from snr.config import Config
from snr.endpoint.endpoint import Endpoint
from snr.endpoint.node_core_endpoint import TASK_TYPE_TERMINATE
from snr.factory import Factory
from snr.io.recorder.factory import RecorderFactory
from snr.node import Node
from snr.runner.test_runner import SynchronusTestRunner
from snr.task import SomeTasks, Task, TaskPriority
from snr.test.utils.expector import Expector
from snr.test.utils.test_base import *


class PingTestEndpoint(Endpoint):
    def __init__(self,
                 factory: Factory,
                 parent_node: Node,
                 name: str,
                 expector: Expector):
        super().__init__(factory,
                         parent_node,
                         name,
                         task_producers=[self.produce_task],
                         task_handlers={
                             "ping_test": self.handle_ping_test,
                             "process_ping_test": self.handle_recv_ping
                         })
        self.parent_node = parent_node
        self.expector = expector
        self.produced_task: bool = False

    def produce_task(self) -> SomeTasks:
        self.expector.call("produce_task")
        if not self.produced_task:
            self.produced_task = True
            return Task("ping_test", priority=TaskPriority.normal)
        return None

    def handle_ping_test(self, t: Task) -> SomeTasks:
        self.expector.call("ping_test")
        self.parent_node.store_data("ping_test", time())
        return None

    def handle_recv_ping(self, t: Task) -> SomeTasks:
        self.expector.call("process_ping_test")
        start = self.parent_node.get_data("ping_test")
        self.info("DDS ping latency: {} ms",
                  [(time() - float(start)) * 1000])
        return Task(TASK_TYPE_TERMINATE, TaskPriority.high, ["all"])


class PingTestFactory(Factory):
    def __init__(self, expector: Expector):
        super().__init__("Ping test factory")
        self.expector = expector

    def get(self, parent_node: Node) -> Endpoint:
        return PingTestEndpoint(self,
                                parent_node,
                                "ping_test_endpoint",
                                self.expector)


class TestInternalDDSPing(SNRTestBase):

    def test_internal_dds_ping(self):
        expector = Expector({
            "ping_test": 1,
            "process_ping_test": 1,
        })
        config = Config({
            "test": [PingTestFactory(expector),
                     RecorderFactory("test_dds_internal_ping_recorder",
                                     ["ping_test", "process_ping_test"])]
        })
        runner = SynchronusTestRunner(config, self.stdout)
        runner.run()
        expector.assert_satisfied(self)


if __name__ == '__main__':
    unittest.main()
