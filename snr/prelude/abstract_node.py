from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from .abstract_component import AbstractComponent
from .abstract_config import AbstractConfig
from .abstract_context import AbstractContext
from .mode import Mode
from .names import ComponentName, Role
from .page import DataKey, Page
from .task import SomeTasks, Task, TaskHandler, TaskId, TaskType


class AbstractNode(AbstractContext, ABC):

    role: Role
    config: AbstractConfig
    mode: Mode
    components: Dict[ComponentName, AbstractComponent]

    @abstractmethod
    def loop(self) -> None:
        ...

    @abstractmethod
    def get_new_tasks(self) -> SomeTasks:
        """Retrieve tasks from endpoints and queue them.
        """
        ...

    @abstractmethod
    def get_task_handlers(self,
                          task: Task,
                          ) -> List[Tuple[TaskHandler, TaskId]]:
        ...

    @abstractmethod
    def handle_task(self,
                    handler: TaskHandler,
                    task: Task,
                    key: TaskId,
                    ) -> Optional[List[Task]]:
        ...

    @abstractmethod
    def execute_task(self, t: Task) -> None:
        ...

    @abstractmethod
    def set_terminate_flag(self, reason: str) -> None:
        ...

    @abstractmethod
    def terminate(self) -> None:
        """Execute actions needed to deconstruct a Node.
        Terminate is executed the main thread or process of an object.
        Conversely, join may be called from an external context such as
        another thread or process.
        """
        ...

    @abstractmethod
    def is_terminated(self) -> bool:
        ...

    @abstractmethod
    def schedule(self, t: SomeTasks) -> None:
        ...

    @abstractmethod
    def page(self,
             key: DataKey,
             data: Any,
             process: bool = True,
             ) -> Page:
        '''Page constructor
        '''
        return Page(key, data,
                    self.name,
                    self.timer.current_s(),
                    process)

    def store_data(self,
                   key: DataKey,
                   data: Any,
                   process: bool = True,
                   ) -> None:
        '''Thread-safe method for constructing a page and scheduling a task to
        store it.
        '''
        self.schedule(Task(TaskType.store_data,
                           key,
                           [data, process]))

    @abstractmethod
    def get_page(self, key: DataKey) -> Optional[Page]:
        '''Thread-safe accesor for pages.
        '''
        ...

    def get_data(self, key: DataKey) -> Optional[Any]:
        '''Thread-safe accessor for plain data, wraps `get_page()`
        '''
        page = self.get_page(key)
        if page:
            return page.data
        return None

    @abstractmethod
    def synchronous_store(self, page: Page) -> None:
        '''Only for synchronous task handlers:
         Writes directely to the Node's datastore.
        For use by [synchronous] node core endpoints to write pages to the
        datastore from the main thread event loop. Not for use by Loops
        running outside the main thread, such as ThreadLoops.
        '''
        ...

    @abstractmethod
    def get_time_s(self) -> float:
        ...

    @abstractmethod
    def dump_data(self) -> str:
        ...
