from __future__ import annotations

from typing import Any, Callable, List, Optional, Tuple

from snr_core.context.context import Context
from snr_core.task import Task, TaskHandler, TaskHandlerMap, TaskId, TaskSource


class EndpointBase(Context):
    def __init__(self,
                 factory: Any,
                 parent_node: Any,
                 name: str,
                 start: Callable[[], None],
                 terminate: Callable[[], None],
                 task_producers: List[TaskSource] = [],
                 task_handlers: TaskHandlerMap = {},
                 ) -> None:
        super().__init__(name, parent_node)
        self.factory = factory
        self.parent_node = parent_node
        self.task_producers = task_producers
        self.task_handlers = task_handlers
        self.start = start
        self.terminate = terminate

    def get_task_handler(self,
                         t: Task
                         ) -> Tuple[Optional[TaskHandler], TaskId]:
        id = t.id()
        (handler, key) = (self.task_handlers.get(id), id)
        if not handler:
            (handler, key) = (self.task_handlers.get(t.type), t.type)
            # self.dbg("Handler for {} not found, using type handler {}",
            #          [t.id(), handler])
        return (handler, key)

    def reload(self, parent_node: Any) -> EndpointBase:
        self.factory.reload()
        new_endpoint = self.factory.get(parent_node)
        return new_endpoint

    def __repr__(self) -> str:
        return self.name
