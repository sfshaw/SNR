import unittest
from typing import List

from snr.config import ComponentsByRole, Config, Mode
from snr.endpoint.dummy import DummyEndpoint
from snr.endpoint.endpoint import Endpoint
from snr.endpoint.factory import EndpointFactory
from snr.node import Node


class TestStringMethods(unittest.TestCase):
    class TestFac(EndpointFactory):
        def __init__(self):
            pass

        def get(self, parent_node: Node) -> List[Endpoint]:
            return [DummyEndpoint(parent_node)]

    def test_empty(self):
        with self.assertRaises(Exception):
            Config()

    def test_one_fac(self):
        components: ComponentsByRole = {"test_role": [self.TestFac()]}
        config = Config(factories=components)
        self.assertEqual(config.get(Mode.TEST), components)

    def test_getter(self):
        self.called: bool = False

        def getter(s: str) -> ComponentsByRole:
            self.called = True
            return {}

        self.assertEqual(Config(get_factories=getter).get("test_mode"), {})
        self.assertTrue(self.called)


if __name__ == '__main__':
    unittest.main()
