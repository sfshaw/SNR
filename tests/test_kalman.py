from snr import *


class TestKalman(SNRTestCase):

    def test_kalman(self):
        with self.temp_file("raw_data.csv"
                            ) as input, \
            self.temp_file("pages.tmp"
                           ) as output1, \
            self.temp_file(filename="filtered_ouput.tmp"
                           ) as output2:

            with input.open() as f:
                f.write("1,2,3\n")
                f.write("4,5,6\n")

            with self.expector({
                (TaskType.process_data, "raw_data"): 2,
            }) as expector:

                self.run_test_node([
                    TextReplayerFactory(input.path,
                                        "raw_data"),
                    RecorderFactory(output1.path, ["raw_data"]),
                    ExpectorEndpointFactory(expector,
                                            exit_when_satisfied=True),
                ])

            output1.assertExists()

            with self.expector({
                (TaskType.process_data, "raw_data"): 2,
                (TaskType.process_data, "filtered_data"): 2,
            }) as expector:

                self.run_test_node([
                    ReplayerFactory(output1.path),
                    KalmanFilterFactory("raw_data", "filtered_data"),
                    RecorderFactory(output2.path, ["filtered_data"]),
                    ExpectorEndpointFactory(
                        expector, exit_when_satisfied=True),
                ])

            output2.assertExists()
            with self.get_context() as context:
                with PageReader(context,
                                "test_reader",
                                output2.path) as reader:
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


if __name__ == '__main__':
    unittest.main()
