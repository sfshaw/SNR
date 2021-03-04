import multiprocessing as mp
import socket
import time

from snr import *
from snr.core.utils.sockets.sockets_wrapper import SocketsWrapper


class TestSocketsLsitener(SNRTestCase):

    @pytest.mark.timeout(0.500)
    def test_sockets_listener_recv(self) -> None:

        data_key = "my_data"
        addr = ("localhost", 54459)

        page = Page(data_key, "data", "origin", 0.75)
        expectations: Expectations = {
            (TaskType.process_data, data_key): 1
        }

        with MPExpector(expectations, self) as expector:

            factories = [
                SocketsListenerFactory(addr[1]),
                ExpectorEndpointFactory(expector,
                                        exit_when_satisfied=True),
            ]
            proc = mp.Process(target=self.run_test_node,
                              args=(factories,))
            proc.start()
            time.sleep(0.025)
            with socket.create_connection(addr) as client:
                sock = SocketsWrapper((client, addr), self.get_context())
                sock.send(page.serialize())

            proc.join(0.100)
            try:
                self.assertFalse(proc.is_alive())
            except AssertionError as e:
                proc.terminate()
                raise e

    @pytest.mark.timeout(0.500)
    def test_sockets_listener_send(self) -> None:

        data_key = "my_data"
        addr = ("localhost", 54459)
        page = Page(data_key, "data", "origin", 0.75)
        expectations: Expectations = {
            (TaskType.process_data, data_key): 1
        }

        with MPExpector(expectations, self) as expector:

            factories = [
                SocketsListenerFactory(addr[1], [data_key]),
                ExpectorEndpointFactory(expector,
                                        exit_when_satisfied=True),
            ]
            proc = mp.Process(target=self.run_test_node,
                              args=(factories,))
            proc.start()
            time.sleep(0.025)
            with socket.create_connection(addr) as client:
                sock = SocketsWrapper((client, addr), self.get_context())
                sock.send(page.serialize())
                response = sock.recv()
                assert response
                self.assertPage(Page.deserialize(response),
                                page.key,
                                page.data,
                                page.origin,
                                page.created_at_s,
                                page.process)

            proc.join(0.100)
            try:
                self.assertFalse(proc.is_alive())
            except AssertionError as e:
                proc.terminate()
                raise e


if __name__ == '__main__':
    unittest.main()
