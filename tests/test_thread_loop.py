from snr import *


class ThreadLoopUnderTest(ThreadLoop):
    __test__ = False

    def __init__(self,
                 factory: LoopFactory,
                 parent: AbstractNode,
                 expector: ExpectorProtocol,
                 ) -> None:
        super().__init__(factory, parent, "thread_loop_under_test")
        self.expector = expector

    def setup(self) -> None:
        self.expector.call("setup")

    def loop(self) -> None:
        pass

    def halt(self) -> None:
        self.expector.call("halt")

    def terminate(self) -> None:
        self.expector.call("terminate")


class TestThreadLooopFactory(LoopFactory):
    __test__ = False

    def __init__(self, expector: ExpectorProtocol) -> None:
        self.expector = expector

    def get(self, parent: AbstractNode) -> ThreadLoop:
        return ThreadLoopUnderTest(self, parent, self.expector)


class TestThreadLoop(SNRTestCase):

    def test_thread_loop(self):

        with self.expector({
            "setup": 1,
            "halt": 1,
            "terminate": 1
        }) as expector:
            self.run_test_node([
                TestThreadLooopFactory(expector),
                TimeoutLoopFactory(ms=10),
            ])
