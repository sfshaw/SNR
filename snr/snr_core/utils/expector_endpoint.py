from snr.snr_core.base import *
from snr.snr_core.utils.expector_protocol import ExpectorProtocol


class ExpectorEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: NodeProtocol,
                 expector: ExpectorProtocol,
                 exit_when_done: bool,
                 ) -> None:
        super().__init__(factory,
                         parent,
                         "expector")
        self.task_handlers: TaskHandlerMap = {}
        for key in expector.get_expectations():
            self.task_handlers[key] = self.call
        self.expector = expector
        self.exit_when_done = exit_when_done

    def task_source(self) -> None:
        return None

    def start(self) -> None:
        pass

    def terminate(self) -> None:
        pass

    def call(self, t: Task, key: TaskId) -> SomeTasks:
        self.dbg(f"Expector called for: {key}")
        self.expector.call(key)
        if self.exit_when_done and self.expector.check():
            return task.terminate("expector_satisfied")
        return None


class ExpectorEndpointFactory(EndpointFactory):
    def __init__(self,
                 expector: ExpectorProtocol,
                 exit_when_done: bool = False
                 ) -> None:
        super().__init__()
        self.expector = expector
        self.exit_when_done = exit_when_done

    def get(self, parent: NodeProtocol) -> EndpointProtocol:
        return ExpectorEndpoint(self,
                                parent,
                                self.expector,
                                self.exit_when_done)
