from __future__ import annotations

from typing import Any, Dict, List

from snr.context.context import Context
from snr.task import TaskHandler, TaskSource


class Endpoint(Context):
    def __init__(self,
                 factory: Any,
                 parent_node: Any,
                 name: str,
                 task_producers: List[TaskSource] = [],
                 task_handlers: Dict[str, TaskHandler] = {}
                 ) -> None:
        super().__init__(name, parent_node)
        self.factory = factory
        self.parent_node = parent_node
        self.task_producers = task_producers
        self.task_handlers = task_handlers

    def start(self) -> None:
        pass

    def set_terminate_flag(self, reason: str) -> None:
        # Stub for synchronous endpoints
        pass

    def terminate(self) -> None:
        self.warn("{} does not implement terminate()",
                  [self.name])
        raise NotImplementedError

    def join(self) -> None:
        # Stub for synchronous endpoints
        return

    def reload(self, parent_node: Any) -> Endpoint:
        self.factory.reload()
        new_endpoint = self.factory.get(parent_node)
        return new_endpoint

    def __repr__(self) -> str:
        return self.name
