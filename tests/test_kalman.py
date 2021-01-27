from snr import *

raw_data_filename = "tests/test_data/in/raw_kalman_data.csv"


class TestKalman(SNRTestBase):

    def test_kalman(self):

        with self.temp_file() as temp_file:
            self.run_test([
                RawDataReplayerFactory(raw_data_filename,
                                       "raw_data",
                                       exit=True),
                RecorderFactory(temp_file.path, ["raw_data"])
            ])

            # self.run_test([
            #     ReplayerFactory(temp_filename, exit=True),
            #     KalmanFilterFactory("raw_data", "filtered_data"),
            #     RecorderFactory("recorder", ["filtered_data"])
            # ])


if __name__ == '__main__':
    unittest.main()
