from __future__ import annotations

from typing import Any

from snr_core.endpoint.endpoint_base import EndpointBase
from snr_core.task import SomeTasks, Task, TaskId, TaskType
from snr_core.utils.utils import no_op

NODE_CORE_NAME_SUFFIX = "_core_endpoint"

TASK_TYPE_LIST_ENDPOINTS = "list_endpoints"


class NodeCore(EndpointBase):
    def __init__(self,
                 factory: Any,
                 parent_node: Any
                 ) -> None:
        super().__init__(factory,
                         parent_node,
                         parent_node.name + NODE_CORE_NAME_SUFFIX,
                         self.start,
                         no_op,
                         task_handlers={
                             TaskType.terminate: self.task_handler_terminate,
                             TaskType.reload: self.task_handler_reload,
                             (TaskType.event, "cmd_list_endpoints"):
                             self.task_handler_list_endpoints,
                         })

    def start(self) -> None:
        # Must implement interface since SynchronousEndpoint cannot be imported
        pass

    def task_producer(self) -> SomeTasks:
        # Must implement interface since SynchronousEndpoint cannot be imported
        return None

    def task_handler_terminate(self, t: Task, key: TaskId) -> SomeTasks:
        # if ("all" in t.val_list
        #         or self.parent_node.name in t.val_list
        #         or "node" in t.val_list):
        self.parent_node.set_terminate_flag(f"terminate_task:{t.name}")
        return None

    def task_handler_reload(self, t: Task, key: TaskId) -> SomeTasks:
        endpoint_name = t.val_list[0]
        endpoint = self.parent_node.endpoints.get(endpoint_name)
        if isinstance(endpoint, EndpointBase):
            self.info("Reloading endoint: {}", [endpoint_name])
            self.parent_node.endpoints[endpoint_name] = endpoint.reload(self)
        else:
            self.warn("Endpoint {} not found", [endpoint_name])

        return None

    def task_handler_list_endpoints(self, t: Task, key: TaskId):
        self.info("Listing endpoints:")
        for name in self.parent_node.endpoints.keys():
            self.info("\t{}", [name])
        self.debugger.flush()
