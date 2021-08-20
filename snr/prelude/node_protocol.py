from typing import Any, List, Optional, Protocol, Tuple

from .task import SomeTasks, Task, TaskHandler, TaskId
from .page import Page, DataKey


class NodeProtocol(Protocol):

    def loop(self) -> None:
        ...

    def get_new_tasks(self) -> SomeTasks:
        """Retrieve tasks from endpoints and queue them.
        """
        ...

    def get_task_handlers(self,
                          task: Task,
                          ) -> List[Tuple[TaskHandler, TaskId]]:
        ...

    def handle_task(self,
                    handler: TaskHandler,
                    task: Task,
                    key: TaskId,
                    ) -> Optional[List[Task]]:
        ...

    def execute_task(self, t: Task) -> None:
        ...

    def set_terminate_flag(self, reason: str) -> None:
        ...

    def terminate(self) -> None:
        """Execute actions needed to deconstruct a Node.
        Terminate is executed the main thread or process of an object.
        Conversely, join may be called from an external context such as
        another thread or process.
        """
        ...

    def is_terminated(self) -> bool:
        ...

    def schedule(self, t: SomeTasks) -> None:
        ...

    def page(self,
             key: DataKey,
             data: Any,
             process: bool = True,
             ) -> Page:
        '''Page constructor
        '''
        ...

    def store_data(self,
                   key: DataKey,
                   data: Any,
                   process: bool = True,
                   ) -> None:
        '''Thread-safe method for constructing a page and scheduling a task to
        store it.
        '''
        ...

    def get_page(self, key: DataKey) -> Optional[Page]:
        '''Thread-safe accesor for pages.
        '''
        ...

    def get_data(self, key: DataKey) -> Optional[Any]:
        '''Thread-safe accessor for plain data, wraps `get_page()`
        '''
        ...

    def synchronous_store(self, page: Page) -> None:
        '''Only for synchronous task handlers:
         Writes directely to the Node's datastore.
        For use by [synchronous] node core endpoints to write pages to the
        datastore from the main thread event loop. Not for use by Loops
        running outside the main thread, such as ThreadLoops.
        '''
        ...

    def get_time_s(self) -> float:
        ...

    def dump_data(self) -> str:
        ...
