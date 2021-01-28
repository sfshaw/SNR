from threading import Event
from typing import Any, Dict, List, Optional, Tuple

from snr_types import *

from snr_protocol.endpoint_protocol import EndpointProtocol
from snr_protocol.factory_protocol import FactoryProtocol
from snr_protocol.loop_protocol import LoopProtocol
from snr_protocol.settings_provider import SettingsProvider


@runtime_checkable
class NodeProtocol(SettingsProvider, Protocol):
    settings: Settings
    name: str
    role: Role
    mode: Mode
    endpoints: Dict[str, EndpointProtocol]
    loops: Dict[str, LoopProtocol]
    is_terminated: Event

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

    def get_components(self,
                       factories: List[FactoryProtocol]
                       ) -> Tuple[Dict[str, EndpointProtocol],
                                  Dict[str, LoopProtocol]]:
        ...

    def schedule(self, t: SomeTasks) -> None:
        ...

    def store_data(self, key: str, data: Any, process: bool = True) -> None:
        ...

    def store_page(self, page: Page) -> None:
        ...

    def get_data(self, key: str) -> Optional[Any]:
        ...

    def get_page(self, key: str) -> Optional[Page]:
        ...
