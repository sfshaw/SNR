import os

from snr import *

raw_data_filename = "tests/test_data/in/raw_kalman_data.csv"


class TestKalman(SNRTestBase):

    def test_kalman(self):

        temp_filename = f"{self.id()}.temp"

        self.assertFalse(os.path.exists(temp_filename))
        try:
            self.run_test([
                RawDataReplayerFactory(raw_data_filename,
                                       "raw_data",
                                       exit=True),
                RecorderFactory(temp_filename, ["raw_data"])
            ])

            # self.run_test([
            #     ReplayerFactory(temp_filename, exit=True),
            #     KalmanFilterFactory("raw_data", "filtered_data"),
            #     RecorderFactory("recorder", ["filtered_data"])
            # ])
        finally:
            os.remove(temp_filename)


if __name__ == '__main__':
    unittest.main()
