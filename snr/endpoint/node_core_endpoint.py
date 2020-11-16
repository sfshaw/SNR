from typing import Any

from snr.endpoint.endpoint import Endpoint
from snr.task import SomeTasks, Task

TASK_TYPE_TERMINATE = "terminate"
TASK_TYPE_RELOAD_ENDPOINT = "reload"
TASK_TYPE_LIST_ENDPOINTS = "list_endpoints"


class NodeCore(Endpoint):
    def __init__(self,
                 factory: None,
                 parent_node: Any
                 ) -> None:
        super().__init__(factory,
                         parent_node,
                         parent_node.name + "core_endpoint",
                         task_handlers={
                             TASK_TYPE_TERMINATE:
                             self.task_handler_terminate,
                             TASK_TYPE_RELOAD_ENDPOINT:
                             self.task_handler_reload,
                             TASK_TYPE_LIST_ENDPOINTS:
                             self.task_handler_list_endpoints,
                         })

    def task_producer(self) -> SomeTasks:
        return None

    def task_handler_terminate(self, t: Task) -> SomeTasks:
        if ("all" in t.val_list
                or self.parent_node.name in t.val_list
                or "node" in t.val_list):
            self.parent_node.set_terminate_flag("terminate_task")
        return None

    def task_handler_reload(self, t: Task) -> SomeTasks:
        endpoint_name = t.val_list[0]
        endpoint = self.parent_node.endpoints.get(endpoint_name)
        if isinstance(endpoint, Endpoint):
            self.info("Reloading endoint: {}", [endpoint_name])
            self.parent_node.endpoints[endpoint_name] = endpoint.reload(self)
        else:
            self.warn("Endpoint {} not found", [endpoint_name])

        return None

    def task_handler_list_endpoints(self, t: Task):
        self.info("Listing endpoints:")
        for name in self.parent_node.endpoints.keys():
            self.info("{}", [name])
        self.debugger.flush()
