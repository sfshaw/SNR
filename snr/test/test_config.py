import unittest

from snr.config import ComponentsByRole, Config
from snr.endpoint import EndpointFactory
from snr.node import Node


class TestStringMethods(unittest.TestCase):
    class TestFac(EndpointFactory):
        def __init__(self):
            pass

        def get(self, parent_node: Node):
            return [None]

    def test_empty(self):
        with self.assertRaises(Exception):
            Config()

    def test_one_fac(self):
        components: ComponentsByRole = {"test_role": [self.TestFac()]}
        config = Config(factories=components)
        self.assertEqual(config.get("test_mode"), components)

    def test_getter(self):
        self.called: bool = False

        def getter(s: str) -> ComponentsByRole:
            self.called = True
            return {}

        self.assertEqual(Config(get_factories=getter).get("test_mode"), {})
        self.assertTrue(self.called)


if __name__ == '__main__':
    unittest.main()
