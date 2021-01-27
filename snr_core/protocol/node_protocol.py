from threading import Event
from typing import Any, Dict, List, Optional, Protocol, Tuple

from snr_core.datastore.page import Page
from snr_core.modes import Mode, Role
from snr_core.protocol.endpoint_protocol import EndpointProtocol
from snr_core.protocol.loop_protocol import LoopProtocol
from snr_core.protocol.settings_provider import SettingsProvider
from snr_core.settings import Settings
from snr_core.task import SomeTasks, Task, TaskHandler, TaskId


class NodeProtocol(SettingsProvider, Protocol):
    settings: Settings
    name: str
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
