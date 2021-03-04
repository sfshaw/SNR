import socket
import threading

from snr import *
from snr.core.utils.sockets.sockets_header import pack_size
from snr.core.utils.sockets.sockets_wrapper import SocketsWrapper


class TestSocketsLoop(SNRTestCase):

    @pytest.mark.timeout(0.500)
    def test_sockets_wrapper(self) -> None:

        def serve(socket: socket.SocketType,
                  page: Page,
                  trigger: threading.Event
                  ) -> None:
            conn, _ = socket.accept()
            data = page.serialize()
            conn.send(pack_size(data))
            conn.send(data)
            conn.close()
            trigger.set()

        page = Page("key", "data", "origin", 0.75)

        with self.create_server(('', 0)) as server_socket:
            addr = server_socket.getsockname()
            with socket.create_connection(addr) as client_socket:
                trigger = threading.Event()
                server_thread = threading.Thread(target=serve,
                                                 args=(server_socket,
                                                       page,
                                                       trigger))
                server_thread.start()
                sw = SocketsWrapper((client_socket, addr), self.get_context())
                sw.open()
                trigger.wait()
                self.assertTrue(sw.poll(0.005))
                new_page = Page.deserialize(sw.recv())
                self.assertPage(new_page,
                                page.key,
                                page.data,
                                page.origin,
                                page.created_at_s,
                                page.process)
                sw.close()
                server_thread.join()


if __name__ == '__main__':
    unittest.main()
