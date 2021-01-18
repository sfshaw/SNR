from snr_core.task import TaskType
from snr_core.runner.test_runner import SynchronusTestRunner
from snr_core.test.utils.expector import Expector
from snr_core.test.utils.expector_endpoint import ExpectorEndpointFactory
from snr_core.test.utils.test_base import *
from snr_core.test.utils.timeout_endpoint import TimeoutEndpointFactory

raw_data_filename = "snr/test/test_data/raw_data.txt"


class TestExpectorEndpoint(SNRTestBase):

    def test_expector_endpoint_empty(self):
        with Expector({}, self) as expector:
            config = self.get_config([
                ExpectorEndpointFactory(expector),
                TimeoutEndpointFactory(seconds=0.5)
            ])
            config.mode = Mode.DEBUG
            runner = SynchronusTestRunner(config)
            runner.run()

    def test_expector_endpoint_terminate(self):
        with Expector({
                TaskType.terminate: 1
        }, self) as expector:
            config = self.get_config([
                ExpectorEndpointFactory(expector),
                TimeoutEndpointFactory(seconds=0.5)
            ])
            runner = SynchronusTestRunner(config)
            runner.run()


if __name__ == '__main__':
    unittest.main()
