from snr import *
from snr.std_mods.utils.timeout_loop_factory import FAST_TEST_TIMEOUT_MS


class LoopUnderTest(ThreadLoop):
    def __init__(self,
                 fac: LoopFactory,
                 parent: AbstractNode,
                 expector: Expector,
                 ) -> None:
        super().__init__(fac,
                         parent,
                         "test_loop",)
        self.expector = expector

    def setup(self) -> None:
        self.expector.call("setup")

    def loop(self) -> None:
        pass

    def halt(self) -> None:
        self.expector.call("halt")

    def terminate(self) -> None:
        self.expector.call("terminate")


class LUTFactory(LoopFactory):
    def __init__(self, expector: Expector) -> None:
        super().__init__()
        self.expector = expector

    def get(self, parent: AbstractNode) -> ThreadLoop:
        return LoopUnderTest(self, parent, self.expector)


class TestLoop(SNRTestCase):

    def test_loop_terminate(self):
        expectations: Expectations = {
            "setup": 1,
            "halt": 1,
            "terminate": 1,
        }
        with Expector(expectations, self) as expector:
            config = self.get_config([
                LUTFactory(expector),
                TimeoutLoopFactory(ms=FAST_TEST_TIMEOUT_MS)
            ])
            runner = TestRunner(config)
            runner.run()
