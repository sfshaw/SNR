from time import time

from snr_core import task
from snr_core.endpoint.endpoint import Endpoint, EndpointBase
from snr_core.endpoint.endpoint_factory import EndpointFactory
from snr_core.factory.factory_base import FactoryBase
from snr_core.node import Node
from snr_core.task import SomeTasks, Task, TaskId, TaskType
from snr_core.test.utils.expector_endpoint import ExpectorEndpointFactory
from snr_core.test.utils.test_base import *


class PingTestEndpoint(Endpoint):
    def __init__(self,
                 factory: FactoryBase,
                 parent_node: Node,
                 name: str):
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
        self.produced_task: bool = False

    def produce_task(self) -> SomeTasks:
        if not self.produced_task:
            self.produced_task = True
            return task.event("ping_test")
        return None

    def handle_ping_test(self, t: Task, key: TaskId) -> SomeTasks:
        self.parent_node.store_data("ping_test", time())
        return None

    def handle_recv_ping(self, t: Task, key: TaskId) -> SomeTasks:
        start = self.parent_node.get_data("ping_test")
        self.info("Datastore ping latency: {} ms",
                  [(time() - float(start)) * 1000])
        return task.terminate("test_endpoint_done")


class PingTestFactory(EndpointFactory):
    def __init__(self):
        super().__init__("Ping test factory")

    def get(self, parent: Node) -> EndpointBase:
        return PingTestEndpoint(self,
                                parent,
                                "ping_test_endpoint")


class TestInternalDatastorePing(SNRTestBase):

    def test_internal_dds_ping(self):
        with self.expector({
            (TaskType.event, "ping_test"): 1,
            (TaskType.process_data, "ping_test"): 1,
            TaskType.terminate: 1,
        }) as expector:
            self.run_test([
                PingTestFactory(),
                ExpectorEndpointFactory(expector),
            ])


if __name__ == '__main__':
    unittest.main()
