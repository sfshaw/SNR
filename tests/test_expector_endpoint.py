from snr import *
from snr.snr_std.utils.timeout_loop_factory import FAST_TEST_TIMEOUT_MS


class TestExpectorEndpoint(SNRTestCase):

    def test_expector_endpoint_empty(self):
        with Expector({}, self) as expector:
            config = self.get_config([
                ExpectorEndpointFactory(expector),
                TimeoutLoopFactory(ms=FAST_TEST_TIMEOUT_MS)
            ])
            config.mode = Mode.DEBUG
            runner = TestRunner(config)
            runner.run()

    def test_expector_endpoint_terminate(self):
        expectations: Expectations = {
            TaskType.terminate: 1,
        }
        with Expector(expectations, self) as expector:
            config = self.get_config([
                ExpectorEndpointFactory(expector),
                TimeoutLoopFactory(ms=FAST_TEST_TIMEOUT_MS)
            ])
            runner = TestRunner(config)
            runner.run()


if __name__ == '__main__':
    unittest.main()
