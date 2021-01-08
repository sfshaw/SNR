from snr.config import TestConfig
from snr.runner.test_runner import SynchronusTestRunner
from snr.test.utils.expector import Expector
from snr.test.utils.expector_endpoint import ExpectorEndpointFactory
from snr.test.utils.test_base import *
from snr.test.utils.timeout_endpoint import TimeoutEndpointFactory

raw_data_filename = "snr/test/test_data/raw_data.txt"


class TestExpectorEndpoint(SNRTestBase):

    def test_expector_endpoint(self):
        expector = Expector({})
        config = TestConfig([
            ExpectorEndpointFactory(expector),
            TimeoutEndpointFactory(seconds=1)
        ])

        runner = SynchronusTestRunner(config, self.stdout)
        runner.run()
        expector.assert_satisfied(self)


if __name__ == '__main__':
    unittest.main()
