import socket
import threading

from snr import *
from snr.std.comms.sockets import sockets_header
from snr.std.comms.sockets.sockets_loop_factory import SocketsLoopFactory


class TestSocketsLoop(SNRTestCase):

    @pytest.mark.timeout(0.500)
    def test_sockets_loop(self) -> None:

        def serve(socket: socket.SocketType,
                  page: Page,
                  trigger: threading.Event
                  ) -> None:
            conn, _ = socket.accept()
            data = page.serialize().encode()
            conn.send(sockets_header.pack_size(data))
            conn.send(data)
            conn.close()
            trigger.set()

        data_key = "my_data"
        addr = ("localhost", 54459)

        page = Page(data_key, "data", "origin", 0.75)
        expectations: Expectations = {
            (TaskType.process_data, data_key): 1
        }

        with MPExpector(expectations, self) as expector, \
            socket.create_server(addr) as server_socket, \
                socket.create_connection(addr) as client_socket:

            trigger = threading.Event()
            server_thread = threading.Thread(target=serve,
                                             args=(server_socket,
                                                   page,
                                                   trigger))
            server_thread.start()
            trigger.wait()
            self.run_test_node([
                SocketsLoopFactory((client_socket, addr), []),
                ExpectorEndpointFactory(expector,
                                        exit_when_satisfied=True),
            ])

            server_thread.join()


if __name__ == '__main__':
    unittest.main()
