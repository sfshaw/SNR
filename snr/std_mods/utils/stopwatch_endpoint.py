from typing import List

from snr.core import *
from snr.interfaces import *
from snr.type_defs import *


class StopwatchEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 times: List[float]
                 ) -> None:
        super().__init__(factory, parent, "stopwatch_endpoint")
        self.task_handlers = {TaskType.process_data: self.task_handler}
        self.times = times

    def task_handler(self, task: Task, key: TaskId) -> SomeTasks:
        self.times.append(self.parent.get_time_s())
        return None

    def begin(self) -> None:
        pass

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass
