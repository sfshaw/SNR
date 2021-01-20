from typing import List

import jsons
from snr_core.endpoint.synchronous_endpoint import Endpoint
from snr_core.endpoint.factory import FactoryBase
from snr_core.node import Node
from snr_core.task import SomeTasks, Task, TaskHandlerMap, TaskType

FILE_EXTENSION = ".txt"
DATA_STORAGE_TASK_HEADER = "process_"


class Recorder(Endpoint):
    def __init__(self,
                 factory: FactoryBase,
                 parent: Node,
                 name: str,
                 data_names: List[str]):
        super().__init__(factory, parent, name,
                         task_handlers=self.map_handlers(data_names))
        self.file = open(self.name + FILE_EXTENSION, "w")

    def task_handler(self, t: Task) -> SomeTasks:
        self.dbg("Recording task: {}", [t])
        if DATA_STORAGE_TASK_HEADER in t.name:
            page = self.parent_node.datastore.get_page(
                t.name[len(DATA_STORAGE_TASK_HEADER):])
            self.file.write(jsons.dumps(page))
        else:
            self.file.write(jsons.dumps(t))
        return None

    def map_handlers(self,
                     data_names: List[str]
                     ) -> TaskHandlerMap:
        handlers: TaskHandlerMap = {}
        for data_name in data_names:
            handlers[(TaskType.event, data_name)] = self.task_handler
        return handlers

    def terminate(self) -> None:
        self.file.close()
