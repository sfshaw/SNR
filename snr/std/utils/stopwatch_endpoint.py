from snr.core.base import *


class StopwatchEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: NodeProtocol,
                 times: List[float]
                 ) -> None:
        super().__init__(factory, parent, "stopwatch_endpoint")
        self.task_handlers = {TaskType.process_data: self.task_handler}
        self.times = times

    def task_handler(self, task: Task, key: TaskId) -> SomeTasks:
        self.times.append(self.parent.get_time_s())
        return None
