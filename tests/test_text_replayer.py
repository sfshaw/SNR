from snr import *


class TestTextReplayer(SNRTestCase):

    def test_raw_reader(self):
        with self.temp_file() as file:

            with file.open() as f:
                f.write("line1\n")
                f.write("line2\n")

            with self.get_context() as context:
                reader = TextReader(context, "test_reader", file.path)
                try:
                    self.assertEqual("line1", reader.read())
                    self.assertEqual("line2", reader.read())
                    self.assertIsNone(reader.read())
                finally:
                    reader.close()

    def test_raw_data_replayer_none(self):
        with self.expector({
            TaskType.terminate: 1,
        }) as expector:
            with self.temp_file() as temp_file:
                with temp_file.open() as f:
                    f.write("")
                self.run_test_node([
                    TextReplayerFactory(temp_file.path,
                                        "raw_data",
                                        exit=True),
                    ExpectorEndpointFactory(expector)
                ])

    def test_raw_data_replayer_one(self):
        with self.expector({
            (TaskType.process_data, "raw_data"): 1,
        }) as expector:

            with self.temp_file() as temp_file:

                with temp_file.open() as f:
                    f.write("whatever")

                self.run_test_node([
                    TextReplayerFactory(temp_file.path,
                                        "raw_data"),
                    ExpectorEndpointFactory(expector,
                                            exit_when_satisfied=True)
                ])

    def test_raw_data_replayer_two(self):
        with self.expector({
            (TaskType.process_data, "raw_data"): 2,
        }) as expector:

            with self.temp_file() as temp_file:

                with temp_file.open() as f:
                    f.write("test_data1\n")
                    f.write("test_data2\n")

                self.run_test_node([
                    TextReplayerFactory(temp_file.path,
                                        "raw_data"),
                    ExpectorEndpointFactory(expector,
                                            exit_when_satisfied=True)
                ])
