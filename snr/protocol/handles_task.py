from typing import Optional, Tuple

from snr.type_defs import *
from typing_extensions import Protocol, runtime_checkable

from .component_protocol import ComponentProtocol


@runtime_checkable
class HandlesTasks(ComponentProtocol, Protocol):

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
