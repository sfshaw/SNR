from typing import Any, Dict, List, Optional, Tuple

from snr.type_defs import *
from snr.type_defs.task import *
from typing_extensions import Protocol, runtime_checkable

from .component_protocol import ComponentProtocol
from .context_protocol import ContextProtocol
from .endpoint_protocol import EndpointProtocol
from .factory_protocol import FactoryProtocol


@runtime_checkable
class NodeProtocol(ContextProtocol, ComponentProtocol, Protocol):
    role: Role
    mode: Mode
    endpoints: Dict[str, EndpointProtocol]

    def loop(self) -> None:
        ...

    def get_task_handlers(self, t: Task) -> List[Tuple[TaskHandler, TaskId]]:
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

    def add_component(self, factory: FactoryProtocol) -> Optional[str]:
        '''Get the component from the factory and store it. Does not call
        begin() on components.
        '''
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
        return Page(key, data,
                    self.name,
                    self.timer.current_s(),
                    process)

    def task_store_data(self,
                        key: DataKey,
                        data: Any,
                        process: bool = True,
                        ) -> Task:
        return task_store_page(self.page(key, data, process))

    def store_page(self, page: Page) -> None:
        '''Thread-safe method for scheduling a task to store a page.
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
        self.store_page(self.page(key, data, process))

    def synchronous_store(self, page: Page) -> None:
        '''Only for synchronous task handlers:
         Writes directely to the Node's datastore.
        For use by [synchronous] node core endpoints to write pages to the
        datastore from the main thread event loop. Not for use by Loops
        running outside the main thread, such as ThreadLoops.
        '''
        ...

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

    def get_time_s(self) -> float:
        ...

    def dump_data(self) -> str:
        ...
