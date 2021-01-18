from snr import *
from snr_test import *

raw_data_filename = "snr/test/test_data/raw_data.txt"


class TestRawDataReplayer(SNRTestBase):

    def test_raw_data_replayer(self):
        with Expector({
            # (TaskType.process_data, "raw_data"): 1
        },
                self) as expector:
            config: Config = self.get_config(
                [RawDataReplayerFactory(raw_data_filename,
                                        "raw_data",
                                        exit=True),
                 ExpectorEndpointFactory(expector)
                 ])
            runner = SynchronusTestRunner(config)
            runner.run()


if __name__ == '__main__':
    unittest.main()
