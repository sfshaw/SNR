from snr import *


class TestTextReader(SNRTestCase):

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


if __name__ == '__main__':
    unittest.main()
