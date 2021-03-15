from snr import *


class TestTextReader(SNRTestCase):

    def test_raw_reader(self):
        with self.temp_file() as file:

            with file.open() as f:
                f.write("line1\n")
                f.write("line2\n")

            with TextReader(self.get_context(),
                            "test_reader",
                            file.path) as reader:
                try:
                    self.assertEqual("line1", reader.read())
                    self.assertEqual("line2", reader.read())
                    self.assertIsNone(reader.read())
                finally:
                    reader.close()
