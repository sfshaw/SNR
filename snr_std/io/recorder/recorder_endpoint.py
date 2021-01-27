from typing import List

from snr_core.base import *


class RecorderEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: NodeProtocol,
                 name: str,
                 filename: str,
                 data_names: List[str]):
        super().__init__(factory, parent, name,
                         task_handlers=self.map_handlers(data_names))
        self.filename = filename
        self.file = open(filename, "w")

    def task_handler(self, t: Task, k: TaskId) -> SomeTasks:
        self.dbg("Recording task: %s", [t])
        if t.type is TaskType.process_data:
            page = self.parent.get_page(t.name)
            if page:
                json_data: str = page.to_json()
                self.file.write(json_data)
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

    def terminate(self) -> None:
        self.file.close()
