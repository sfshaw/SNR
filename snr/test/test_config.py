import unittest

from snr.config import Config


class TestStringMethods(unittest.TestCase):

    def test_no_components(self):
        with self.assertRaises(Exception):
            config = Config()


if __name__ == '__main__':
    unittest.main()
