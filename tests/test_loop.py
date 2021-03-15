from typing import Callable, Optional

from snr import *


class InvalidLoopNoSetup(ThreadLoop):
    def __init__(self, factory: LoopFactory, parent: AbstractNode) -> None:
        super().__init__(factory, parent, "invalid_loop_no_setup")

    def loop(self) -> None:
        pass

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass


class InvalidLoopNoLoop(ThreadLoop):
    def __init__(self, factory: LoopFactory, parent: AbstractNode) -> None:
        super().__init__(factory, parent, "invalid_loop_no_loop")

    def setup(self) -> None:
        pass

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass


class InvalidLoopNoHalt(ThreadLoop):
    def __init__(self, factory: LoopFactory, parent: AbstractNode) -> None:
        super().__init__(factory, parent, "invalid_loop_no_halt")

    def setup(self) -> None:
        pass

    def loop(self) -> None:
        pass

    def terminate(self) -> None:
        pass


class InvalidLoopNoTerminate(ThreadLoop):
    def __init__(self, factory: LoopFactory, parent: AbstractNode) -> None:
        super().__init__(factory, parent, "invalid_loop_no_terminate")

    def setup(self) -> None:
        pass

    def loop(self) -> None:
        pass

    def halt(self) -> None:
        pass


class ValidLoop(ThreadLoop):
    def __init__(self,
                 fac: LoopFactory,
                 parent: AbstractNode,
                 expector: Optional[ExpectorProtocol],
                 ) -> None:
        super().__init__(fac, parent, "test_loop",)
        self.expector = expector

    def setup(self) -> None:
        if self.expector:
            self.expector.call("setup")

    def loop(self) -> None:
        if self.expector:
            self.expector.call("loop")

    def halt(self) -> None:
        if self.expector:
            self.expector.call("halt")

    def terminate(self) -> None:
        if self.expector:
            self.expector.call("terminate")


class ValidLoopFactory(LoopFactory):
    def __init__(self, expector: Optional[ExpectorProtocol] = None) -> None:
        super().__init__()
        self.expector = expector

    def get(self, parent: AbstractNode) -> ThreadLoop:
        return ValidLoop(self, parent, self.expector)


class TestLoop(SNRTestCase):

    def test_invalid_construction_fails(self) -> None:
        fac = ValidLoopFactory()
        node = self.mock_node()

        def construct(invalid_constructor: Callable[
            [LoopFactory, AbstractNode, None],
            None
        ]) -> None:
            invalid_constructor(fac, node, None)

        self.assertRaises(TypeError,
                          construct,
                          InvalidLoopNoSetup)  # type: ignore
        self.assertRaises(TypeError,
                          construct,
                          InvalidLoopNoLoop)  # type: ignore
        self.assertRaises(TypeError,
                          construct,
                          InvalidLoopNoHalt)  # type: ignore
        self.assertRaises(TypeError,
                          construct,
                          InvalidLoopNoTerminate)  # type: ignore

    def test_valid_construction(self) -> None:
        valid_loop: ThreadLoop = ValidLoop(ValidLoopFactory(),
                                           self.mock_node(),
                                           None)
        self.assertTrue(isinstance(valid_loop,
                                   AbstractComponent))  # type: ignore
        self.assertTrue(isinstance(valid_loop,
                                   AbstractLoop))  # type: ignore

    def test_loop_methods(self):
        expectations: OrderedExpectations = [
            "setup",
            "loop",
            "halt",
            "terminate",
        ]
        with self.ordered_expector(expectations) as expector:
            config = self.get_config([
                ValidLoopFactory(expector),
                TimeoutLoopFactory()
            ])
            runner = TestRunner(config)
            runner.run()
