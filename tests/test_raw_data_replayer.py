from snr import *


class TestRawDataReplayer(SNRTestBase):

    def test_raw_reader(self):
        with self.temp_file() as file:

            with file.open() as f:
                f.write("line1\n")
                f.write("line2\n")

            reader = RawReader(self.context(), "test_reader", file.path)
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
                self.run_test([
                    RawDataReplayerFactory(temp_file.path,
                                           "raw_data",
                                           exit=True),
                    ExpectorEndpointFactory(expector)
                ])

    def test_raw_data_replayer_one(self):
        with self.expector({
            (TaskType.process_data, "raw_data"): 1,
            TaskType.terminate: 1,
        }) as expector:

            with self.temp_file() as temp_file:

                with temp_file.open() as f:
                    f.write("test_data\n")

                self.run_test([
                    RawDataReplayerFactory(temp_file.path,
                                           "raw_data",
                                           exit=True),
                    ExpectorEndpointFactory(expector)
                ])

    def test_raw_data_replayer_two(self):
        with self.expector({
            (TaskType.process_data, "raw_data"): 2,
            TaskType.terminate: 1,
        }) as expector:

            with self.temp_file() as temp_file:

                with temp_file.open() as f:
                    f.write("test_data1\n")
                    f.write("test_data2\n")
                    f.write("\n")

                self.run_test([
                    RawDataReplayerFactory(temp_file.path,
                                           "raw_data",
                                           exit=True),
                    ExpectorEndpointFactory(expector)
                ])


if __name__ == '__main__':
    unittest.main()
