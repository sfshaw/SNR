import logging
from typing import List

from snr_core.endpoint.endpoint import Endpoint
from snr_core.factory.factory_base import FactoryBase
from snr_core.node import Node
from snr_core.task import SomeTasks, Task, TaskHandlerMap, TaskId, TaskType


class RecorderEndpoint(Endpoint):
    def __init__(self,
                 factory: FactoryBase,
                 parent: Node,
                 name: str,
                 data_names: List[str]):
        super().__init__(factory, parent, name,
                         task_handlers=self.map_handlers(data_names))
        self.file = open(self.name, "w")
        self.log.setLevel(logging.DEBUG)

    def task_handler(self, t: Task, k: TaskId) -> SomeTasks:
        self.dbg("Recording task: %s", [t])
        if t.type is TaskType.process_data:
            page = self.parent.get_page(t.name)
            if page:
                self.file.write(page.to_json())
            else:
                self.err("Tried to read non-existant page: %s", t.name)
        else:
            self.file.write(t.to_json())
        return None

    def map_handlers(self,
                     data_names: List[str]
                     ) -> TaskHandlerMap:
        handlers: TaskHandlerMap = {}
        for data_name in data_names:
            handlers[(TaskType.process_data, data_name)] = self.task_handler
            handlers[(TaskType.event, data_name)] = self.task_handler
        return handlers

    def terminate(self) -> None:
        self.file.close()
