from snr import *

raw_data_filename = "snr/test/test_data/raw_kalman_data.csv"


class TestKalman(SNRTestBase):

    def test_kalman(self):
        # config = self.get_config([
        #     RawDataReplayerFactory(raw_data_filename, "raw_data", exit=True),
        #     RecorderFactory("raw_data_recorder", ["raw_data"])
        # ])

        # runner = SynchronusTestRunner(config)
        # runner.run()

        # config = self.get_config([
        #     ReplayerFactory("raw_data_recorder.txt", exit=True),
        #     KalmanFilterFactory("raw_data", "filtered_data"),
        #     RecorderFactory("recorder", ["filtered_data"])
        # ])
        # runner = SynchronusTestRunner(config)
        # runner.run()
        pass


if __name__ == '__main__':
    unittest.main()
