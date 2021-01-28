from snr_std.io.replayer.replayer import PageReader
from snr import *

raw_data_filename = "tests/test_data/in/raw_kalman_data.csv"


class TestKalman(SNRTestBase):

    def test_kalman(self):
        with self.temp_file() as temp_file:

            with self.expector({
                (TaskType.process_data, "raw_data"): 2,
                (TaskType.terminate, "replayer_done"): 1,
            }) as expector:

                self.run_test_node([
                    RawDataReplayerFactory(raw_data_filename,
                                           "raw_data",
                                           exit=True),
                    RecorderFactory(temp_file.path, ["raw_data"]),
                    ExpectorEndpointFactory(expector),
                ])

            temp_file.assertExists()

            with self.expector({
                (TaskType.process_data, "raw_data"): 2,
                (TaskType.terminate, "replayer_done"): 1,
            }) as expector:

                with self.temp_file(filename="filtered_ouput.tmp") as output:

                    self.run_test_node([
                        ReplayerFactory(temp_file.path, exit=True),
                        KalmanFilterFactory("raw_data", "filtered_data"),
                        RecorderFactory(output.path, ["filtered_data"]),
                        ExpectorEndpointFactory(expector),
                    ])

                    output.assertExists()
                    reader = PageReader(self.root_context,
                                        "test_reader",
                                        output.path)
                    self.assertPage(reader.read(),
                                    "filtered_data",
                                    "1,2,3",
                                    "test_node",
                                    process=True)
                    self.assertPage(reader.read(),
                                    "filtered_data",
                                    "4,5,6",
                                    "test_node",
                                    process=True)
                    self.assertIsNone(reader.read())
                    reader.close()


if __name__ == '__main__':
    unittest.main()
