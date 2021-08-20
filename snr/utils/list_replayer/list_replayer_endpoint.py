import logging
from typing import Any, List

from snr.core import *
from snr.prelude import *

NAME_PREFIX: str = "list_replayer_loop_"


class ListReplayerEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 data: List[Any],
                 data_name: DataKey,
                 exit_when_done: bool
                 ) -> None:
        super().__init__(factory,
                         parent,
                         NAME_PREFIX + data_name)
        self.log.setLevel(logging.WARNING)
        self.bootstrap_task_name = "start_list_replayer_" + data_name
        self.task_handlers = {
            (TaskType.event, self.bootstrap_task_name): self.read_item,
            (TaskType.process_data, data_name): self.read_item,
        }
        self.data_name = data_name
        self.iter = iter(data)
        self.done: bool = False
        self.exit_when_done = exit_when_done

    def begin(self):
        self.parent.schedule(tasks.event(self.bootstrap_task_name))

    def read_item(self, task: Task, key: TaskId) -> SomeTasks:
        if not self.done:
            try:
                item = next(self.iter)
                self.dbg("Read line: %s", item)
                return self.parent.task_store_data(self.data_name, item)
            except StopIteration:
                self.dbg("Replayer Done")
                self.done = True
                if self.exit_when_done:
                    self.dbg("Replayer scheduling terminate task")
                    return tasks.terminate("list_replayer_done")
        return None

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass
