from typing import Callable, Optional

from snr import *


class InvalidEndpointNoBegin(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 ) -> None:
        super().__init__(factory, parent, "invalid_endpoint_no_begin")

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass


class InvalidEndpointNoHalt(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 ) -> None:
        super().__init__(factory, parent, "invalid_endpoint_no_halt")

    def begin(self) -> None:
        pass

    def terminate(self) -> None:
        pass


class InvalidEndpointNoTerminate(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 ) -> None:
        super().__init__(factory, parent, "invalid_endpoint_no_terminate")

    def begin(self) -> None:
        pass

    def halt(self) -> None:
        pass


class ValidEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 expector: Optional[ExpectorProtocol],
                 ) -> None:
        super().__init__(factory, parent, "endpoint_under_test")
        self.task_handlers: TaskHandlerMap = {}
        self.expector = expector

    def begin(self) -> None:
        if self.expector:
            self.expector.call("begin")

    def halt(self) -> None:
        if self.expector:
            self.expector.call("halt")

    def terminate(self) -> None:
        if self.expector:
            self.expector.call("terminate")


class ValidEndpointFactory(EndpointFactory):
    def __init__(self, expector: Optional[ExpectorProtocol] = None) -> None:
        super().__init__()
        self.expector = expector

    def get(self, parent: AbstractNode) -> Endpoint:
        return ValidEndpoint(self, parent, self.expector)


class TestEndpoint(SNRTestCase):

    def test_invalid_construction_fails(self):
        fac = ValidEndpointFactory()
        node = self.mock_node()

        def construct(invalid_constructor: Callable[
            [EndpointFactory,
             AbstractNode,
             Optional[ExpectorProtocol]], None],
        ) -> None:
            invalid_constructor(fac, node, None)

        self.assertRaises(TypeError,
                          construct,
                          InvalidEndpointNoBegin)  # type: ignore
        self.assertRaises(TypeError,
                          construct,
                          InvalidEndpointNoHalt)  # type: ignore
        self.assertRaises(TypeError,
                          construct,
                          InvalidEndpointNoTerminate)  # type: ignore

    def test_valid_construction(self):
        valid_endpoint = ValidEndpoint(ValidEndpointFactory(),
                                       self.mock_node(),
                                       None)
        self.assertTrue(isinstance(valid_endpoint,
                                   AbstractComponent))  # type: ignore
        self.assertTrue(isinstance(valid_endpoint,
                                   AbstractEndpoint))  # type: ignore

    def test_endpoint_methods(self):
        expectations = {
            "begin": 1,
            "halt": 1,
            "terminate": 1,
        }
        with self.expector(expectations) as expector:
            self.run_test_node([
                TimeoutLoopFactory(),
                ValidEndpointFactory(expector),
            ])
