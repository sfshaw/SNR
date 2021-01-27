
from snr_core.base import *
from snr_core.test.utils.expector_endpoint import ExpectorEndpointFactory
from snr_core.test.utils.timeout_loop import (FAST_TEST_TIMEOUT_MS,
                                              TimeoutLoopFactory)

raw_data_filename = "snr/test/test_data/raw_data.txt"


class TestExpectorEndpoint(SNRTestBase):

    def test_expector_endpoint_empty(self):
        with Expector({}, self) as expector:
            config = self.get_config([
                ExpectorEndpointFactory(expector),
                TimeoutLoopFactory(ms=FAST_TEST_TIMEOUT_MS)
            ])
            config.mode = Mode.DEBUG
            runner = SynchronusTestRunner(config)
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
            runner = SynchronusTestRunner(config)
            runner.run()


if __name__ == '__main__':
    unittest.main()
