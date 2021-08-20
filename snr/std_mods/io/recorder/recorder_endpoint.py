import logging
from typing import Dict, List

from snr.core import *
from snr.prelude import *


class RecorderEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 name: ComponentName,
                 filename: str,
                 data_keys: List[DataKey]):
        super().__init__(factory, parent, name)
        self.log.setLevel(logging.WARNING)
        self.task_handlers = self.map_handlers(data_keys)
        self.data_keys = data_keys
        self.filename = filename
        self.file = open(filename, "w")

    def task_source(self) -> None:
        return None

    def task_handler(self, t: Task, k: TaskId) -> SomeTasks:
        self.dbg("Recording task: %s", [t])
        if ((t.type is TaskType.store_data) and
                (t.name in self.data_keys)):
            page = t.val_list[0]
            if isinstance(page, Page):
                json_data = page.serialize().decode()
                self.file.write(json_data)
                self.file.write("\n")
                self.file.flush()
                self.dbg("Wrote '%s' to %s", json_data, self.filename)
            else:
                self.warn("Task did not contain valid page: %s", t.name)
        else:
            self.warn("Tried non-data processing task: %s", t.name)
        return None

    def map_handlers(self,
                     data_keys: List[DataKey],
                     ) -> TaskHandlerMap:
        handlers: Dict[TaskId, TaskHandler] = {}
        for key in data_keys:
            handlers[(TaskType.store_data, key)] = self.task_handler
        return handlers

    def begin(self) -> None:
        pass

    def halt(self) -> None:
        self.file.flush()

    def terminate(self) -> None:
        self.file.close()
        self.info("Closing file %s", self.filename)
