import unittest

from snr_core.config import Components, Config, Mode
from snr_core.endpoint.dummy import DummyEndpointFactory


class TestConfig_(unittest.TestCase):

    def test_empty(self):
        with self.assertRaises(Exception):
            Config(Mode.TEST, {})

    def test_one_fac(self):
        factories: Components = [DummyEndpointFactory()]
        config = Config(Mode.TEST, {"test": factories})
        self.assertEqual(config.get("test"), factories)

    def test_two_facs(self):
        factories: Components = [
            DummyEndpointFactory("dummy1"),
            DummyEndpointFactory("dummy2")
        ]
        config = Config(Mode.TEST, {"test": factories})
        self.assertEqual(config.get("test"), factories)


if __name__ == '__main__':
    unittest.main()
