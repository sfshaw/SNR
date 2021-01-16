from snr.task import TaskType
from snr.runner.test_runner import SynchronusTestRunner
from snr.test.utils.expector import Expector
from snr.test.utils.expector_endpoint import ExpectorEndpointFactory
from snr.test.utils.test_base import *
from snr.test.utils.timeout_endpoint import TimeoutEndpointFactory

raw_data_filename = "snr/test/test_data/raw_data.txt"


class TestExpectorEndpoint(SNRTestBase):

    def test_expector_endpoint(self):
        with Expector({TaskType.terminate: 1}, self) as expector:
            config = self.get_config([
                ExpectorEndpointFactory(expector),
                TimeoutEndpointFactory(seconds=0.5)
            ])

            runner = SynchronusTestRunner(config)
            runner.run()


if __name__ == '__main__':
    unittest.main()
