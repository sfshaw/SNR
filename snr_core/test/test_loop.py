from snr_core.loop.loop_factory import LoopFactory
from snr_core.loop.thread_loop import ThreadLoop
from snr_core.node import Node
from snr_core.runner.test_runner import SynchronusTestRunner
from snr_core.test.utils.expector import Expectations, Expector
from snr_core.test.utils.test_base import *
from snr_core.test.utils.timeout_loop import TimeoutLoopFactory
from snr_core.utils.utils import no_op


class LoopUnderTest(ThreadLoop):
    def __init__(self,
                 fac: LoopFactory,
                 parent: Node,
                 expector: Expector
                 ) -> None:
        super().__init__(fac, parent, "test_loop",
                         no_op,
                         self.setup,
                         self.terminate)
        self.expector = expector

    def setup(self) -> None:
        self.expector.call("start")

    def terminate(self) -> None:
        self.expector.call("terminate")


class LUTFactory(LoopFactory):
    def __init__(self, expector: Expector) -> None:
        super().__init__("test_factory")
        self.expector = expector

    def get(self, parent: Node) -> ThreadLoop:
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
                TimeoutLoopFactory(0.1)
            ])
            runner = SynchronusTestRunner(config)
            runner.run()


if __name__ == '__main__':
    unittest.main()
