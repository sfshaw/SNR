import logging
from snr import *
from snr.snr_core.runner.multi_proc_runner import MultiProcRunner
from snr.snr_std.utils.timeout_loop_factory import FAST_TEST_TIMEOUT_MS


class TestMultiProcRunner(SNRTestCase):

    def test_proc_runner(self) -> None:
        logging.getLogger().setLevel(logging.DEBUG)
        fac = TimeoutLoopFactory(ms=FAST_TEST_TIMEOUT_MS)
        config = Config(
            Mode.TEST, {"test1": [fac],
                        "test2": [fac]})
        runner: MultiRunnerProtocol = MultiProcRunner(config,
                                                      ["test1", "test2"])
        runner.run()


if __name__ == '__main__':
    unittest.main()
