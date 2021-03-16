import logging

from snr.core import *
from snr.interfaces import *
from snr.type_defs import *


class MovingAvgEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 name: ComponentName,
                 input: DataKey,
                 output: DataKey,
                 filter: MovingAvgFilter,
                 ) -> None:
        super().__init__(factory, parent, name)
        self.log.setLevel(logging.WARNING)
        self.input = input
        self.output = output
        self.task_handlers = {
            (TaskType.store_page, self.input): self.update_filter,
        }
        self.filter = filter

    def update_filter(self, task: Task, key: TaskId) -> SomeTasks:
        if not (task.name == self.input and
                isinstance(task.val_list[0], Page) and
                (isinstance(task.val_list[0].data, float) or
                 isinstance(task.val_list[0].data, int))):
            self.warn("Invalid data from %s", task)
            return None
        self.filter.update(task.val_list[0].data)
        return tasks.store_page(self.parent.page(self.output,
                                                 self.filter.avg()))

    def begin(self) -> None:
        pass

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass
