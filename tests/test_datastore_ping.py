import logging
import time

from snr import *


class PingTestEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent_node: AbstractNode,
                 name: ComponentName):
        super().__init__(factory,
                         parent_node,
                         name)
        self.log.setLevel(logging.WARNING)
        self.task_handlers: TaskHandlerMap = {
            (TaskType.event, "ping_request"):
            self.store_ping,
            (TaskType.process_data, "ping"):
            self.process_ping
        }
        self.produced_task: bool = False

    def begin(self) -> None:
        self.parent.schedule(tasks.event("ping_request"))

    def store_ping(self, t: Task, key: TaskId) -> SomeTasks:
        self.parent.store_data("ping", time.time())
        self.dbg("Storing ping page")
        return None

    def process_ping(self, t: Task, key: TaskId) -> SomeTasks:
        data = self.parent.get_data("ping")
        if not isinstance(data, float):
            self.err("Stored ping data %s was not a float", data)
            return None
        start: float = data
        self.info("Datastore ping latency: %s ms",
                  (time.time() - float(start)) * 1000)
        return tasks.terminate("test_endpoint_done")

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass


class PingTestFactory(EndpointFactory):
    def __init__(self):
        super().__init__()

    def get(self, parent: AbstractNode) -> AbstractEndpoint:
        return PingTestEndpoint(self,
                                parent,
                                "ping_test_endpoint")


class TestDatastorePing(SNRTestCase):

    def test_dds_ping(self):
        expectations: TaskExpectations = {
            (TaskType.event, "ping_request"): 1,
            (TaskType.store_data, "ping"): 1,
            (TaskType.process_data, "ping"): 1,
            TaskType.terminate: 1,
        }
        with self.expector(expectations) as expector:
            self.run_test_node([
                PingTestFactory(),
                ExpectorEndpointFactory(expector),
            ])
