from typing import Callable, Dict, List
from snr.context import Context
from snr.task import TaskHandler


class Endpoint(Context):
    def __init__(self,
                 parent_context: Context,
                 name: str,
                 task_producers: List[Callable] = [],
                 task_handlers: Dict[str, TaskHandler] = {}
                 ):
        super().__init__(name, parent_context)
        self.task_producers = task_producers
        self.task_handlers = task_handlers

    def set_terminate_flag(self, reason: str):
        # Stub for synchronous endpoints
        pass

    def terminate(self):
        self.warn("{} does not implement terminate()",
                  [self.name])
        raise NotImplementedError

    def join(self):
        # Stub for synchronous endpoints
        return

    def __repr__(self) -> str:
        return self.name
