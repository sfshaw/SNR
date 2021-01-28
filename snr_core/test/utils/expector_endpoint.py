from snr_core.base import *
from snr_core.test.utils.expector import Expector


class ExpectorEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: NodeProtocol,
                 expector: Expector
                 ) -> None:
        super().__init__(factory,
                         parent,
                         "expector")
        self.task_handlers: TaskHandlerMap = {}
        for key in expector.expectations:
            self.task_handlers[key] = self.call
        self.expector = expector

    def task_source(self) -> None:
        return None

    def start(self) -> None:
        pass

    def terminate(self) -> None:
        pass

    def call(self, task: Task, key: TaskId) -> SomeTasks:
        self.dbg(f"Expector called for: {key}")
        self.expector.call(key)
        return None


class ExpectorEndpointFactory(EndpointFactory):
    def __init__(self, expector: Expector):
        super().__init__(None, "Ping test factory")
        self.expector = expector

    def get(self, parent: NodeProtocol) -> EndpointProtocol:
        return ExpectorEndpoint(self,
                                parent,
                                self.expector)
