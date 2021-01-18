import unittest

from snr.config import Components, Config, Mode
from snr.endpoint.dummy import DummyEndpointFactory


class TestConfig_(unittest.TestCase):

    def test_empty(self):
        with self.assertRaises(Exception):
            Config(Mode.TEST, {})

    def test_one_fac(self):
        factories: Components = [DummyEndpointFactory()]
        config = Config(Mode.TEST, {"test": factories})
        self.assertEqual(config.get("test"), factories)


if __name__ == '__main__':
    unittest.main()
