from __future__ import annotations

from typing import Any, List

from snr.endpoint.endpoint import Endpoint
from snr.factory import Factory
from snr.node import Node
from snr.task import TaskHandlerMap, TaskSource


class SynchronousEndpoint(Endpoint):
    def __init__(self,
                 factory: Factory,
                 parent: Node,
                 name: str,
                 task_producers: List[TaskSource] = [],
                 task_handlers: TaskHandlerMap = {}
                 ) -> None:
        super().__init__(factory, parent, name, task_producers, task_handlers)

    def start(self) -> None:
        # Stub for synchronous endpoints
        pass

    def terminate(self) -> None:
        self.set_terminate_flag()

    def join(self) -> None:
        self.set_terminate_flag()
        # Stub for synchronous endpoints

    def set_terminate_flag(self):
        # Stub for synchronous endpoints
        pass

    def reload(self, parent_node: Any) -> Endpoint:
        self.factory.reload()
        new_endpoint = self.factory.get(parent_node)
        return new_endpoint

    def __repr__(self) -> str:
        return self.name
