import unittest
from snr import *


class BenchNodeStartup(SNRTestCase):

    def test_node_construction_time(self):
        role = "test"
        config = self.get_config()

        timer = Timer()
        node = Node(role, config)
        t_s = timer.current_s()

        node.terminate()

        self.assertLess(t_s, 0.030, "Node construct time")
        print(f"\nNode construct time: {t_s * 1000:7.3f} ms")


if __name__ == '__main__':
    unittest.main()
