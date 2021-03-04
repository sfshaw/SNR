import socket
import threading

from snr import *


class TestSocketsLoop(SNRTestCase):

    @pytest.mark.timeout(0.500)
    def test_sockets_loop(self) -> None:

        def serve(socket: socket.SocketType,
                  page: Page,
                  trigger: threading.Event
                  ) -> None:
            with self.wrap_socket(socket.accept()) as sw:
                sw.send(page.serialize())
            trigger.set()

        data_key = "my_data"

        page = Page(data_key, "data", "origin", 0.75)
        expectations: Expectations = {
            (TaskType.process_data, data_key): 1
        }

        with MPExpector(expectations, self) as expector, \
                self.create_server(('', 0)) as server_socket:
            addr = server_socket.getsockname()
            with socket.create_connection(addr) \
                    as client_socket:

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
