import logging
from typing import List

from snr.core import *
from snr.protocol import *
from snr.type_defs import *


class RecorderEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: NodeProtocol,
                 name: str,
                 filename: str,
                 data_keys: List[str]):
        super().__init__(factory, parent, name)
        self.task_handlers = self.map_handlers(data_keys)
        self.filename = filename
        self.file = open(filename, "w")
        self.log.setLevel(logging.WARNING)

    def task_source(self) -> None:
        return None

    def task_handler(self, t: Task, k: TaskId) -> SomeTasks:
        self.dbg("Recording task: %s", [t])
        if t.type is TaskType.process_data:
            page = self.parent.get_page(t.name)
            if page:
                json_data = page.serialize().decode()
                self.file.write(json_data)
                self.file.write("\n")
                self.file.flush()
                self.dbg("Wrote '%s' to %s", json_data, self.filename)
            else:
                self.err("Tried to read non-existant page: %s", t.name)
        else:
            self.err("Tried non-data processing task: %s", t.name)
        return None

    def map_handlers(self,
                     data_names: List[str]
                     ) -> TaskHandlerMap:
        handlers: TaskHandlerMap = {}
        for data_name in data_names:
            handlers[(TaskType.process_data, data_name)] = self.task_handler
            handlers[(TaskType.event, data_name)] = self.task_handler
        return handlers

    def join(self) -> None:
        self.file.flush()
        self.file.close()
        self.info("Closing file %s", self.filename)
