from typing import Any, List, Optional, Protocol, Tuple, runtime_checkable

from snr_types import *

from snr_protocol.component_protocol import ComponentProtocol


@runtime_checkable
class EndpointProtocol(ComponentProtocol, Protocol):

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
        if not handler:
            return None
        return (handler, key)

    def start(self) -> None:
        ...

    def terminate(self) -> None:
        ...

    def reload(self, parent: Any) -> Any:
        ...
