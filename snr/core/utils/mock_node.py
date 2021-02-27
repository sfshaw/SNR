from snr.protocol import *
from snr.types import *

from ..base import *
from ..context.root_context import RootContext


class MockNode(RootContext, NodeProtocol):

    def __init__(self) -> None:
        super().__init__("mock_node", None)
        self.role: Role = "test"
        self.mode = Mode.TEST
        self.endpoints: Dict[str, EndpointProtocol] = {}

    def loop(self) -> None:
        pass

    def get_task_handlers(self, t: Task) -> List[Tuple[TaskHandler, TaskId]]:
        return []

    def set_terminate_flag(self, reason: str) -> None:
        pass

    def terminate(self) -> None:
        pass

    def is_terminated(self) -> bool:
        return True

    def add_component(self, factory: FactoryProtocol) -> Optional[str]:
        pass

    def schedule(self, t: SomeTasks) -> None:
        pass

    def store_page(self, page: Page) -> None:
        pass

    def store_data(self, key: str, data: Any, process: bool = True) -> None:
        pass

    def synchronous_store(self, page: Page) -> None:
        pass

    def get_page(self, key: str) -> Optional[Page]:
        pass

    def get_data(self, key: str) -> Optional[Any]:
        pass

    def get_time(self) -> float:
        return 0.0
