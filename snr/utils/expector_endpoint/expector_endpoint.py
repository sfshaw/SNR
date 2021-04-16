import logging
from typing import Dict, List, Mapping

from snr.core import *
from snr.interfaces import *
from snr.type_defs import *

from ..expector_protocol import ExpectorProtocol

TaskExpectations = Mapping[TaskId, int]


class ExpectorEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 name: ComponentName,
                 expector: ExpectorProtocol,
                 exit_when_satisfied: bool,
                 ) -> None:
        super().__init__(factory,
                         parent,
                         name)
        self.log.setLevel(logging.WARNING)
        self.task_handlers: TaskHandlerMap = self.map_handlers(
            expector.get_expectations())
        self.expector = expector
        self.exit_when_satisfied = exit_when_satisfied

    def task_source(self) -> None:
        return None

    def begin(self) -> None:
        pass

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass

    def call(self, t: Task, key: TaskId) -> SomeTasks:
        self.dbg(f"Expector called for: {key}")
        self.expector.call(key)
        if self.exit_when_satisfied and self.expector.check():
            return tasks.terminate("expector_satisfied")
        return None

    def map_handlers(self,
                     data_keys: List[TaskId]
                     ) -> TaskHandlerMap:
        handlers: Dict[TaskId, TaskHandler] = {}
        for key in data_keys:
            handlers[key] = self.call
            self.dbg("Expecting: %s", key)
        return handlers
