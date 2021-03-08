import logging

from snr.core import *

from ..expector_protocol import ExpectorProtocol


class ExpectorEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: NodeProtocol,
                 expector: ExpectorProtocol,
                 exit_when_satisfied: bool,
                 ) -> None:
        super().__init__(factory,
                         parent,
                         "expector")
        self.log.setLevel(logging.WARNING)
        self.task_handlers: TaskHandlerMap = {}
        for key in expector.get_expectations():
            self.dbg("Expecting: %s", key)
            self.task_handlers[key] = self.call
        self.expector = expector
        self.exit_when_satisfied = exit_when_satisfied

    def task_source(self) -> None:
        return None

    def start(self) -> None:
        pass

    def terminate(self) -> None:
        pass

    def call(self, t: Task, key: TaskId) -> SomeTasks:
        self.dbg(f"Expector called for: {key}")
        self.expector.call(key)
        if self.exit_when_satisfied and self.expector.check():
            return task_terminate("expector_satisfied")
        return None
