from time import time

from snr import task
from snr.endpoint.endpoint import Endpoint
from snr.endpoint.endpoint_factory import EndpointFactory
from snr.endpoint.factory import Factory
from snr.endpoint.synchronous_endpoint import SynchronousEndpoint
from snr.node import Node
from snr.runner.test_runner import SynchronusTestRunner
from snr.task import SomeTasks, Task, TaskType
from snr.test.utils.expector import Expector
from snr.test.utils.test_base import *


class PingTestEndpoint(SynchronousEndpoint):
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
                             (TaskType.event, "ping_test"):
                             self.handle_ping_test,
                             (TaskType.process_data, "ping_test"):
                             self.handle_recv_ping
                         })
        self.parent_node = parent_node
        self.expector = expector
        self.produced_task: bool = False

    def produce_task(self) -> SomeTasks:
        self.expector.call("produce_task")
        if not self.produced_task:
            self.produced_task = True
            return task.event("ping_test")
        return None

    def handle_ping_test(self, t: Task) -> SomeTasks:
        self.expector.call("ping_test")
        self.parent_node.store_data("ping_test", time())
        return None

    def handle_recv_ping(self, t: Task) -> SomeTasks:
        self.expector.call("process_ping_test")
        start = self.parent_node.get_data("ping_test")
        self.info("Datastore ping latency: {} ms",
                  [(time() - float(start)) * 1000])
        return task.terminate("test_endpoint_done")


class PingTestFactory(EndpointFactory):
    def __init__(self, expector: Expector):
        super().__init__("Ping test factory")
        self.expector = expector

    def get(self, parent: Node) -> Endpoint:
        return PingTestEndpoint(self,
                                parent,
                                "ping_test_endpoint",
                                self.expector)


class TestInternalDatastorePing(SNRTestBase):

    def test_internal_dds_ping(self):
        with Expector({
                "ping_test": 1,
                "process_ping_test": 1},
                self) as expector:
            config = self.get_config([
                PingTestFactory(expector),
                # RecorderFactory("ping_recorder",
                #                 ["ping_test", "process_ping_test"])
            ])
            runner = SynchronusTestRunner(config)
            runner.run()


if __name__ == '__main__':
    unittest.main()
