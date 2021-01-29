import pickle
import socket
import sys
from socket import socket as Socket

from snr.snr_core.base import *


class CommandReceiver(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent: NodeProtocol,
                 name: str,
                 port: int
                 ) -> None:
        super().__init__(factory,
                         parent,
                         name,
                         tick_rate_hz=0)
        self.port = port

    def send(self, data: Page) -> None:
        return None

    def loop_handler(self) -> None:
        with Socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("localhost", self.port))
            sock.listen()
            (connection, _) = sock.accept()
            while not self.is_terminated():
                data_size = int.from_bytes(connection.recv(4),
                                           byteorder=sys.byteorder)
                data: bytes = connection.recv(data_size)
                page: Page = pickle.loads(data)
                self.parent.store_data(page.key, page.data)
