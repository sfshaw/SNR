from threading import Event
from typing import Any, Dict, List, Optional, Protocol, Tuple

from snr_core.context.context import Context
from snr_core.datastore.page import Page
from snr_core.endpoint.endpoint_protocol import EndpointProtocol
from snr_core.loop.loop_protocol import LoopProtocol
from snr_core.modes import Mode, Role
from snr_core.task import SomeTasks, Task, TaskHandler, TaskId


class NodeProtocol(Protocol):
    context: Context
    role: Role
    mode: Mode
    endpoints: Dict[str, EndpointProtocol]
    loops: Dict[str, LoopProtocol]
    is_terminated: Event

    def loop(self):
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

    def schedule(self, t: SomeTasks) -> None:
        ...

    def store_data(self, key: str, data: Any, process: bool = True) -> None:
        ...

    def get_data(self, key: str) -> Optional[Any]:
        ...

    def get_page(self, key: str) -> Optional[Page]:
        ...
