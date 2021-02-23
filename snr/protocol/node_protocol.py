from snr.types import *

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
        ...

    def schedule(self, t: SomeTasks) -> None:
        ...

    def store_page(self, page: Page) -> None:
        ...

    def store_data(self, key: str, data: Any, process: bool = True) -> None:
        ...

    def synchronous_store(self, page: Page) -> None:
        '''For use by node core endpoints to write pages to a the datastore.
        Not for use by Loops running outside the main thread,
        such as ThreadLoops
        '''
        ...

    def get_page(self, key: str) -> Optional[Page]:
        ...

    def get_data(self, key: str) -> Optional[Any]:
        ...

    def get_time(self) -> float:
        ...
