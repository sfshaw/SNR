from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple

from .abstract_context import AbstractContext
from .abstract_factory import AbstractFactory
from .page import DataKey
from .task import Task, TaskHandler, TaskHandlerMap, TaskId


class AbstractComponent(AbstractContext, ABC):

    factory: AbstractFactory[Any]
    task_handlers: TaskHandlerMap

    def get_task_handler(self,
                         task: Task
                         ) -> Optional[Tuple[TaskHandler, TaskId]]:
        """Given a task to handle, get the matching handlers from an
        Endpoint.
                Returns a tuple of the found handler and the key that found it,
        if any.
        """
        id: TaskId = (task.type, task.name)
        handler = self.task_handlers.get(id)
        if handler:
            return (handler, id)

        handler = self.task_handlers.get(task.type)
        if handler:
            return (handler, task.type)
        return None

    @abstractmethod
    def begin(self) -> None:
        ...

    @abstractmethod
    def join(self) -> None:
        ...

    @abstractmethod
    def halt(self) -> None:
        ...

    @abstractmethod
    def terminate(self) -> None:
        ...

    @abstractmethod
    def store_data(self,
                   key: DataKey,
                   data: Any,
                   process: bool = True,
                   ) -> None:
        ...

    @abstractmethod
    def task_source(self) -> List[Task]:
        ...
