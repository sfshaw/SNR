from time import time

from snr_core.base import *
from snr_core.test.utils.base import *


class PingTestEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent_node: NodeProtocol,
                 name: str):
        super().__init__(factory,
                         parent_node,
                         name)
        self.                    task_handlers = {
            (TaskType.event, "ping_test"):
            self.handle_ping_test,
            (TaskType.process_data, "ping_test"):
            self.handle_recv_ping
        }
        self.produced_task: bool = False

    def task_source(self) -> SomeTasks:
        if not self.produced_task:
            self.produced_task = True
            return task.event("ping_test")
        return None

    def handle_ping_test(self, t: Task, key: TaskId) -> SomeTasks:
        self.parent.store_data("ping_test", time())
        return None

    def handle_recv_ping(self, t: Task, key: TaskId) -> SomeTasks:
        data = self.parent.get_data("ping_test")
        if not isinstance(data, float):
            self.err("Stored ping data %s was not a float", data)
            return None
        start: float = data
        self.info("Datastore ping latency: {} ms",
                  [(time() - float(start)) * 1000])
        return task.terminate("test_endpoint_done")


class PingTestFactory(EndpointFactory):
    def __init__(self):
        super().__init__(None, "Ping test factory")

    def get(self, parent: NodeProtocol) -> EndpointProtocol:
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
            self.run_test_node([
                PingTestFactory(),
                ExpectorEndpointFactory(expector),
            ])


if __name__ == '__main__':
    unittest.main()
