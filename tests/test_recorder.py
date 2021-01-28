from snr import *

RAW_DATA_PATH = "tests/test_data/in/raw_data1.txt"


class TestRecorder(SNRTestBase):

    def test_recorder_encoding(self):
        with self.expector({(
            TaskType.process_data, "raw_data"): 1,
            TaskType.terminate: 1
        }) as expector:

            with self.temp_file() as output:

                self.run_test_node([
                    RawDataReplayerFactory(RAW_DATA_PATH,
                                           "raw_data",
                                           exit=True),
                    RecorderFactory(output.path, ["raw_data"]),
                    ExpectorEndpointFactory(expector)
                ])

                output.assertExists()
                with open(output.path) as f:
                    line = f.readline()
                    page = Page.deserialize(line)
                    if page:
                        self.assertEqual("raw_data", page.key)
                        self.assertEqual("test_data", page.data)
                        self.assertEqual("test_node", page.origin)
                    else:
                        self.assertTrue(
                            False,
                            f"Deserialization  of {line} failed, got {page}")


if __name__ == '__main__':
    unittest.main()
