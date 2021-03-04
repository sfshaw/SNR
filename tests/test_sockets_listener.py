import multiprocessing as mp
import socket
import time

from snr import *
from snr.std.comms.sockets import sockets_header


class TestSocketsLsitener(SNRTestCase):

    @pytest.mark.timeout(0.500)
    def test_sockets_listener(self) -> None:

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
            time.sleep(0.050)
            with socket.create_connection(addr) as client:
                data = page.serialize().encode()
                client.send(sockets_header.pack_size(data))
                client.send(data)

            proc.join(0.100)
            try:
                self.assertFalse(proc.is_alive())
            except AssertionError as e:
                proc.terminate()
                raise e


if __name__ == '__main__':
    unittest.main()
