import socket
import threading

import pytest
from snr import *
from snr.std_mods.comms.sockets_base import sockets_header


class TestSocketsLoop(SNRTestCase):

    @pytest.mark.timeout(0.500)
    def test_sockets_wrapper(self) -> None:

        def serve(socket: socket.SocketType,
                  page: Page,
                  trigger: threading.Event
                  ) -> None:
            conn, _ = socket.accept()
            data = page.serialize()
            conn.send(sockets_header.pack_size(data))
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
