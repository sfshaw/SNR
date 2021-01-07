import unittest

from snr.config import ComponentsByRole, Config, Mode
from snr.endpoint.dummy import DummyEndpoint
from snr.endpoint.endpoint import Endpoint
from snr.factory import Factory
from snr.node import Node


class TestConfig(unittest.TestCase):
    class TestFac(Factory):
        def __init__(self):
            pass

        def get(self, parent_node: Node) -> Endpoint:
            return DummyEndpoint(parent_node)

    def test_empty(self):
        with self.assertRaises(Exception):
            Config()

    def test_one_fac(self):
        components: ComponentsByRole = {"test_role": [self.TestFac()]}
        config = Config(factories=components)
        self.assertEqual(config.get(Mode.TEST), components)

    def test_getter(self):
        self.called: bool = False

        def getter(mode: Mode) -> ComponentsByRole:
            self.called = True
            return {}

        self.assertEqual(Config(get_factories=getter).get(Mode.TEST), {})
        self.assertTrue(self.called)


if __name__ == '__main__':
    unittest.main()
