from snr_test import *

raw_data_filename = "snr_test/test_data/in/raw_data.txt"


class TestRawDataReplayer(SNRTestBase):

    def test_raw_data_replayer(self):
        with Expector({
            (TaskType.process_data, "raw_data"): 1,
            TaskType.terminate: 1,
        },
                self) as expector:
            config: Config = self.get_config([
                RawDataReplayerFactory(raw_data_filename,
                                       "raw_data",
                                       exit=True),
                ExpectorEndpointFactory(expector)
            ])
            config.mode = Mode.DEBUG
            runner = SynchronusTestRunner(config)
            runner.run()


if __name__ == '__main__':
    unittest.main()
