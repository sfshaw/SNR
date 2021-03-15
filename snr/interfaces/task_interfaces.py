from abc import ABC, abstractmethod
from typing import Optional, Tuple

from snr.type_defs import *


class ProvidesTaskHandlers(ABC):

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


class ProvidesTasks(ABC):

    @abstractmethod
    def task_source(self) -> SomeTasks:
        ...


class SchedulesTasks(ABC):

    @abstractmethod
    def schedule(self, t: SomeTasks) -> None:
        ...
