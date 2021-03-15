from snr import *


class EndpointUnderTest(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 expector: ExpectorProtocol,
                 ) -> None:
        super().__init__(factory, parent, "endpoint_under_test_b")
        self.expector = expector
        self.task_handlers: TaskHandlerMap = {}

    def call(self) -> None:
        self.expector.call("mod_b")

    def begin(self) -> None:
        pass

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass
