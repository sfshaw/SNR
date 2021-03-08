from snr import *
from snr.std_mods.utils.timeout_loop_factory import FAST_TEST_TIMEOUT_MS


class TestMultiProcRunner(SNRTestCase):

    def test_proc_runner(self) -> None:
        fac = TimeoutLoopFactory(ms=FAST_TEST_TIMEOUT_MS)
        config = Config(
            Mode.TEST, {"test1": [fac],
                        "test2": [fac]})
        runner: MultiRunnerProtocol = MultiProcRunner(config,
                                                      ["test1", "test2"])
        runner.run()
