from snr import *
import pytest


class TestTimeoutLoop(SNRTestCase):

    @pytest.mark.timeout(0.030)
    def test_timeout_loop_ms(self) -> None:
        self.run_test_node([TimeoutLoopFactory(ms=1)])

    @pytest.mark.timeout(0.030)
    def test_timeout_loop_s(self) -> None:
        self.run_test_node([TimeoutLoopFactory(seconds=0.001)])
