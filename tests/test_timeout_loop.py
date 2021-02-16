from snr import *
from snr.snr_std.utils.timeout_loop_factory import FAST_TEST_TIMEOUT_MS


class TestTimeoutLoop(SNRTestCase):

    def test_timeout_loop(self) -> None:
        self.run_test_node([TimeoutLoopFactory(ms=FAST_TEST_TIMEOUT_MS)])


if __name__ == '__main__':
    unittest.main()
