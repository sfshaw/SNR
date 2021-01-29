from typing import Any, Optional, Tuple

from snr.snr_types import *

from snr.snr_protocol.component_protocol import ComponentProtocol


@runtime_checkable
class EndpointProtocol(ComponentProtocol, Protocol):

    name: str
    task_handlers: TaskHandlerMap

    def task_source(self) -> SomeTasks:
        ...

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
