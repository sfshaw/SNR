from __future__ import annotations

from typing import Any, List, Optional

from snr_core.context.context import Context
from snr_core.task import Task, TaskHandler, TaskHandlerMap, TaskSource


class Endpoint(Context):
    def __init__(self,
                 factory: Any,
                 parent_node: Any,
                 name: str,
                 task_producers: List[TaskSource] = [],
                 task_handlers: TaskHandlerMap = {}
                 ) -> None:
        super().__init__(name, parent_node)
        self.factory = factory
        self.parent_node = parent_node
        self.task_producers = task_producers
        self.task_handlers = task_handlers

    def start(self) -> None:
        # Stub for synchronous endpoints
        raise NotImplementedError

    def terminate(self) -> None:
        # Stub for synchronous endpoints
        raise NotImplementedError

    def join(self) -> None:
        # Stub for synchronous endpoints
        raise NotImplementedError

    def set_terminate_flag(self) -> None:
        # Stub for synchronous endpoints
        raise NotImplementedError

    def get_task_handler(self, t: Task) -> Optional[TaskHandler]:
        handler = self.task_handlers.get(t.id())
        if not handler:
            handler = self.task_handlers.get(t.type)
            # self.dbg("Handler for {} not found, using type handler {}",
            #          [t.id(), handler])
        return handler

    def reload(self, parent_node: Any) -> Endpoint:
        self.factory.reload()
        new_endpoint = self.factory.get(parent_node)
        return new_endpoint

    def __repr__(self) -> str:
        return self.name
