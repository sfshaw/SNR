import logging
from typing import Any, Dict, List, Optional, Tuple

from snr.core import *
from snr.interfaces import *
from snr.type_defs import *


class MockTimer(TimerProtocol):
    def __init__(self):
        self.time = 0

    def current_s(self) -> float:
        self.time += 1
        return self.time


class MockNode(RootContext, AbstractNode):

    def __init__(self) -> None:
        super().__init__("mock_node", logging.WARNING)
        self.role: Role = "test"
        self.mode = Mode.TEST
        self.components: Dict[ComponentName, AbstractComponent] = {}
        self.timer = MockTimer()

    def loop(self) -> None:
        pass

    def get_new_tasks(self) -> SomeTasks:
        """Retrieve tasks from endpoints and queue them.
        """
        ...

    def handle_task(self,
                    handler: TaskHandler,
                    task: Task,
                    key: TaskId,
                    ) -> Optional[List[Task]]:
        return None

    def execute_task(self, t: Task) -> None:
        pass

    def get_task_handlers(self,
                          task: Task,
                          ) -> List[Tuple[TaskHandler, TaskId]]:
        return []

    def set_terminate_flag(self, reason: str) -> None:
        pass

    def terminate(self) -> None:
        pass

    def is_terminated(self) -> bool:
        return True

    def add_component(self,
                      factory: AbstractFactory,
                      ) -> Optional[str]:
        pass

    def schedule(self, t: SomeTasks) -> None:
        pass

    def store_page(self, page: Page) -> None:
        pass

    def synchronous_store(self, page: Page) -> None:
        pass

    def task_store_page(self, page: Page) -> Task:
        return tasks.store_page(page)

    def page(self, key: DataKey, data: Any, process: bool = True) -> Page:
        return Page(key, data, self.name,  0, process=process)

    def get_page(self, key: str) -> Optional[Page]:
        pass

    def get_time_s(self) -> float:
        return 0

    def dump_data(self) -> str:
        return "No mock profiling data"
