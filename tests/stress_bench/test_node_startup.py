from snr import *


class TestNodeStartup(SNRTestCase):

    def test_node_construction_time(self):
        role = "test"
        config = self.get_config()

        timer = Timer()
        node = Node(role, config)
        t_s = timer.current_s()

        node.terminate()

        self.assertLess(t_s, 0.010, "Node construct time")
        print(f"Node construct time: {t_s * 1000:7.3f} ms")
