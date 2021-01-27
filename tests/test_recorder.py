from snr import *
from snr_core.test.utils.expector_endpoint import ExpectorEndpointFactory

RAW_DATA_PATH = "tests/test_data/in/raw_data.txt"


class TestRecorder(SNRTestBase):

    def test_recorder_encoding(self):
        with self.temp_file(overwrite=True, cleanup=False) as temp_file:
            with self.expector({(
                TaskType.process_data, "raw_data"): 1,
                TaskType.terminate: 1
            }) as expector:
                self.run_test([
                    RawDataReplayerFactory(RAW_DATA_PATH,
                                           "raw_data",
                                           exit=True),
                    RecorderFactory(temp_file.path, ["raw_data"]),
                    ExpectorEndpointFactory(expector)
                ])
            temp_file.assertExists()
            with open(temp_file.path) as f:
                line = f.readline()
                page = Page.from_json(line)
                self.assertEqual("raw_data", page.key)
                self.assertEqual("test_data", page.data)
                self.assertEqual("test_node", page.origin)


if __name__ == '__main__':
    unittest.main()
