from time import time
from typing import List

from snr.config import Config
from snr.endpoint import Endpoint
from snr.factory import EndpointFactory
from snr.node import TASK_TYPE_TERMINATE, Node
from snr.runner import Runner
from snr.task import SomeTasks, Task, TaskPriority


class PingTestEndpoint(Endpoint):
    def __init__(self,
                 parent_node: Node,
                 name: str):
        super().__init__(
            parent_node,
            name,
            task_producers=[self.produce_task],
            task_handlers={
                "ping_test": self.handle_ping_test,
                "process_ping_test": self.handle_recv_ping
            })
        self.parent_node = parent_node
        self.unused = True

    def produce_task(self) -> SomeTasks:
        if self.unused:
            self.unused = False
            return Task("ping_test", priority=TaskPriority.normal)
        return None

    def handle_ping_test(self, t: Task) -> SomeTasks:
        self.parent_node.store_data("ping_test", time())
        return None

    def handle_recv_ping(self, t: Task) -> SomeTasks:
        start = self.parent_node.get_data("ping_test")
        latency = time() - start
        self.info("DDS ping latency: {}", [latency])
        return Task(TASK_TYPE_TERMINATE, TaskPriority.high, ["all"])


class PingTestFactory(EndpointFactory):
    def __init__(self):
        pass

    def get(self, parent_node: Node) -> List[Endpoint]:
        return [PingTestEndpoint(parent_node, "ping_test_endpoint")]

    def __repr__(self) -> str:
        return "Ping test factory"


runner = Runner(Config(
    components_by_role={
        "test": [PingTestFactory()]
    }))
runner.run()
runner = None
