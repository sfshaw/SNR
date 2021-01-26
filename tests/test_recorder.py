import os

from snr import *

raw_data_filename = "tests/test_data/in/raw_data.txt"


class TestRecorder(SNRTestBase):

    def test_recorder(self):
        TEMP_FILENAME = "temp.rec"
        self.assertFalse(os.path.exists(TEMP_FILENAME))
        try:
            self.run_test([
                RawDataReplayerFactory(raw_data_filename,
                                       "raw_data",
                                       exit=True),
                RecorderFactory(TEMP_FILENAME, ["raw_data"])
            ])

            self.assertTrue(os.path.exists(TEMP_FILENAME))
            with open(TEMP_FILENAME) as f:
                line = f.readline()
                print(f"Read line: {line}")
                page = Page.from_json(line)
                self.assertEqual("raw_data", page.key)
                self.assertEqual("test_data", page.data)
                self.assertEqual("test_node", page.origin)
        finally:
            os.remove(TEMP_FILENAME)


if __name__ == '__main__':
    unittest.main()
