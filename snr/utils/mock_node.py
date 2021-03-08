import logging
from typing import Dict, Tuple

from snr.core import *
from snr.protocol import *


class MockTimer(TimerProtocol):
    def __init__(self):
        self.time = 0

    def current_s(self) -> float:
        self.time += 1
        return self.time


class MockNode(RootContext, NodeProtocol):

    def __init__(self) -> None:
        super().__init__("mock_node", logging.WARNING)
        self.role: Role = "test"
        self.mode = Mode.TEST
        self.endpoints: Dict[str, EndpointProtocol] = {}
        self.timer = MockTimer()

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

    def synchronous_store(self, page: Page) -> None:
        pass

    def get_page(self, key: str) -> Optional[Page]:
        pass
