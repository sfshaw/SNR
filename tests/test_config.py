from typing import List

from snr import *


class TestConfig(SNRTestCase):

    def test_empty(self):
        with self.assertRaises(Exception):
            Config(Mode.TEST, {})

    def test_one_fac(self):
        factories: List[FactoryProtocol] = [DummyEndpointFactory()]
        config = Config(Mode.TEST, {"test": factories})
        self.assertEqual(config.get("test"), factories)

    def test_two_facs(self):
        factories: List[FactoryProtocol] = [
            DummyEndpointFactory("dummy1"),
            DummyEndpointFactory("dummy2")
        ]
        config = Config(Mode.TEST, {"test": factories})
        self.assertEqual(config.get("test"), factories)
