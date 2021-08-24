from abc import ABC, abstractmethod
from typing import Optional

from .abstract_context import AbstractContext
from .task import SomeTasks, Task


class AbstractTaskQueue(AbstractContext, ABC):

    def schedule(self, t: SomeTasks) -> None:
        """ Adds a Task or a list of Tasks to the node's queue
        """
        if isinstance(t, Task):
            self.schedule_task(t)
        elif t:
            # Recursively handle lists
            for item in t:
                if item:
                    self.schedule(item)

    @abstractmethod
    def schedule_task(self, t: Task) -> None:
        ...

    @abstractmethod
    def get_next(self) -> Optional[Task]:
        """Take the next task off the queue
        """
        ...

    @abstractmethod
    def get_new_tasks(self) -> SomeTasks:
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        ...
