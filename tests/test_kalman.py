from snr import *


class TestKalman(SNRTestCase):

    def test_kalman(self):
        with self.temp_file() as input_file, \
                self.temp_file() as intermediate_file, \
                self.temp_file() as output_file:

            with input_file.open() as f:
                f.write("1,2,3,\n")
                f.write("4,5,6,\n")

            with self.expector({
                (TaskType.store_page, "raw_data"): 2,
            }) as expector:

                self.run_test_node([
                    TextReplayerFactory(input_file.path,
                                        "raw_data"),
                    RecorderEndpointFactory(intermediate_file.path,
                                            ["raw_data"]),
                    ExpectorEndpointFactory(expector,
                                            exit_when_satisfied=True),
                ])

            intermediate_file.assertExists()

            with self.expector({
                (TaskType.store_page, "raw_data"): 2,
                (TaskType.store_page, "filtered_data"): 2,
            }) as expector:

                self.run_test_node([
                    ReplayerLoopFactory(intermediate_file.path),
                    KalmanFilterFactory("raw_data", "filtered_data"),
                    RecorderEndpointFactory(output_file.path,
                                            ["filtered_data"]),
                    ExpectorEndpointFactory(expector,
                                            exit_when_satisfied=True),
                ])

            output_file.assertExists()
            with PageReader(self.get_context(),
                            "test_reader",
                            output_file.path) as reader:
                self.assertPage(reader.read(),
                                "filtered_data",
                                "1,2,3,",
                                "test_node",
                                process=True)
                self.assertPage(reader.read(),
                                "filtered_data",
                                "4,5,6,",
                                "test_node",
                                process=True)
                self.assertIsNone(reader.read())
