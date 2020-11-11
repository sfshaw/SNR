import unittest
from time import time
from typing import List

from snr.config import Config
from snr.endpoint.endpoint import Endpoint
from snr.endpoint.factory import EndpointFactory
from snr.node import TASK_TYPE_TERMINATE, Node
from snr.runner.test_runner import SynchronusTestRunner
from snr.task import SomeTasks, Task, TaskPriority
from snr.test.expector import Expector


class PingTestEndpoint(Endpoint):
    def __init__(self,
                 parent_node: Node,
                 name: str,
                 expector: Expector):
        super().__init__(
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


class PingTestFactory(EndpointFactory):
    def __init__(self, expector: Expector):
        self.expector = expector

    def get(self, parent_node: Node) -> List[Endpoint]:
        return [PingTestEndpoint(parent_node,
                                 "ping_test_endpoint",
                                 self.expector)]

    def __repr__(self) -> str:
        return "Ping test factory"


class TestInternalDDSPing(unittest.TestCase):

    def test_internal_dds_ping(self):
        expector = Expector({
            "ping_test": 1,
            "process_ping_test": 1,
        })
        config = Config({
            "test": [PingTestFactory(expector)]
        })
        runner = SynchronusTestRunner(config)
        runner.run()
        expector.assert_satisfied(self)


if __name__ == '__main__':
    unittest.main()
