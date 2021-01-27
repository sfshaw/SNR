from __future__ import annotations

from typing import Any, List, Optional, Protocol, Tuple, runtime_checkable

from snr_core.factory.factory_protocol import Component
from snr_core.task import Task, TaskHandler, TaskHandlerMap, TaskId, TaskSource


@runtime_checkable
class EndpointProtocol(Component, Protocol):

    name: str
    task_producers: List[TaskSource]
    task_handlers: TaskHandlerMap

    def get_task_handler(self,
                         t: Task
                         ) -> Optional[Tuple[TaskHandler, TaskId]]:
        """Given a task to handle, get the matching handlers from an Endpoint.
        Returns a tuple of the found handler and the key that found it, if any.
        """
        id = t.id()
        (handler, key) = (self.task_handlers.get(id), id)
        if not handler:
            (handler, key) = (self.task_handlers.get(t.type), t.type)
            # self.dbg("Handler for {} not found, using type handler {}",
            #          [t.id(), handler])
        if not handler:
            return None
        return (handler, key)

    def start(self) -> None:
        ...

    def terminate(self) -> None:
        ...

    def reload(self, parent: Any) -> EndpointProtocol:
        ...
