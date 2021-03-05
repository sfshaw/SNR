from snr.core.utils.expector_protocol import ExpectorProtocol
from snr import *


class EndpointUnderTest(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: NodeProtocol,
                 expector: ExpectorProtocol,
                 ) -> None:
        super().__init__(factory, parent, "endpoint_under_test_b")
        self.expector = expector
        self.task_handlers: TaskHandlerMap = {}

    def call(self) -> None:
        self.expector.call("mod_b")

    def join(self):
        pass
