from snr import *
from snr_core.test.utils.expector_endpoint import ExpectorEndpointFactory

raw_data_filename = "tests/test_data/in/raw_data.txt"


class TestRawDataReplayer(SNRTestBase):

    def test_raw_reader(self):
        reader = RawReader(self.context(), "test_reader", raw_data_filename)
        try:
            self.assertEqual("test_data", reader.read())
            self.assertIsNone(reader.read())
        finally:
            reader.close()

    def test_raw_data_replayer(self):
        with self.expector({
            (TaskType.process_data, "raw_data"): 1,
            TaskType.terminate: 1,
        }) as expector:
            self.run_test([
                RawDataReplayerFactory(raw_data_filename,
                                       "raw_data",
                                       exit=True),
                ExpectorEndpointFactory(expector)
            ])


if __name__ == '__main__':
    unittest.main()
