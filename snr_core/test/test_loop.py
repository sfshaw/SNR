from snr_core.base import *
from snr_core.test.utils.base import *


class LoopUnderTest(ThreadLoop):
    def __init__(self,
                 fac: LoopFactory,
                 parent: NodeProtocol,
                 expector: Expector,
                 ) -> None:
        super().__init__(fac,
                         parent,
                         "test_loop",)
        self.expector = expector

    def setup(self) -> None:
        self.expector.call("start")

    def terminate(self) -> None:
        self.expector.call("terminate")


class LUTFactory(LoopFactory):
    def __init__(self, expector: Expector) -> None:
        super().__init__("test_factory")
        self.expector = expector

    def get(self, parent: NodeProtocol) -> ThreadLoop:
        return LoopUnderTest(self, parent, self.expector)


class TestLoop(SNRTestBase):

    def test_loop_terminate(self):
        expectations: Expectations = {
            "start": 1,
            "terminate": 1,
        }
        with Expector(expectations, self) as expector:
            config = self.get_config([
                LUTFactory(expector),
                TimeoutLoopFactory(ms=FAST_TEST_TIMEOUT_MS)
            ])
            runner = SynchronusTestRunner(config)
            runner.run()


if __name__ == '__main__':
    unittest.main()
