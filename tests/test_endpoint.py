from snr import *


class EndpointUnderTest(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 expector: ExpectorProtocol,
                 ) -> None:
        super().__init__(factory, parent, "endpoint_under_test")
        self.task_handlers: TaskHandlerMap = {}
        self.expector = expector

    def begin(self) -> None:
        self.expector.call("begin")

    def halt(self) -> None:
        self.expector.call("halt")

    def terminate(self) -> None:
        self.expector.call("terminate")


class EndpointUnderTestFactory(EndpointFactory):
    def __init__(self, expector: ExpectorProtocol) -> None:
        super().__init__()
        self.expector = expector

    def get(self, parent: AbstractNode) -> Endpoint:
        return EndpointUnderTest(self, parent, self.expector)


class TestEndpoint(SNRTestCase):

    def test_endpoint(self):
        expectations = {
            "begin": 1,
            "halt": 1,
            "terminate": 1,
        }
        with self.expector(expectations) as expector:
            self.run_test_node([
                TimeoutLoopFactory(),
                EndpointUnderTestFactory(expector),
            ])
