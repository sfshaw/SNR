from snr.core import *
from snr.protocol import *
from snr.type_defs import *


class MovingAvgEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: NodeProtocol,
                 name: str,
                 input: DataKey,
                 output: DataKey,
                 filter: MovingAvgFilter,
                 ) -> None:
        super().__init__(factory, parent, name)
        self.input = input
        self.output = output
        self.task_handlers = {
            (TaskType.store_page, self.input): self.update_filter,
        }
        self.filter = filter

    def update_filter(self, task: Task, key: TaskId) -> SomeTasks:
        assert (task.name == self.input and
                isinstance(task.val_list[0], Page) and
                isinstance(task.val_list[0].data, float))
        self.filter.update(task.val_list[0].data)
        return task_store_page(self.parent.page(self.output,
                                                self.filter.avg()))
