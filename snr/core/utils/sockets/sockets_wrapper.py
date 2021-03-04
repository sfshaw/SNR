import select
import socket

from snr.core.base import *
from snr.types import *

from . import sockets_header


class SocketsWrapper(Context, ConnectionProtocol):

    def __init__(self,
                 connection: Tuple[socket.socket, Any],
                 parent: ContextProtocol,
                 ) -> None:
        super().__init__("sockets_wrapper", parent.settings, parent.profiler)
        self.connection = connection[0]
        self.something_else = connection[1]
        self.select = select.poll()
        self.log.setLevel(logging.WARNING)

    def open(self) -> None:
        self.select.register(self.connection.fileno(),
                             select.POLLIN)

    def is_closed(self) -> bool:
        return self.connection is None

    def send(self, data: bytes):
        header = sockets_header.pack_size(data)
        self.connection.send(header)
        self.connection.send(data)
        self.dbg("%s send payload of size %s",
                 self.connection.fileno(), header)

    def poll(self, timeout_ms: float) -> bool:
        assert self.connection
        result: List[Tuple[int, int]] = self.select.poll(timeout_ms / 1000)
        self.dbg("Ran poll on %s: %s", self.connection.fileno(), result)
        return ((len(result) > 0) and
                (result[0] == (self.connection.fileno(),
                               select.POLLIN)))

    def recv(self) -> Optional[JsonData]:
        assert self.connection
        try:
            data_len = sockets_header.unpack_size(
                self.connection.recv(sockets_header.PACKET_SIZE_HEADER_LENGTH))
            self.dbg("Prepared to recv %s", data_len)
            data = self.connection.recv(data_len)
            self.dbg("Recevied data on %s", self.connection.fileno())
            return data
        except Exception as e:
            self.warn("Error in Recv: %s", str(e))
            return None

    def close(self) -> None:
        assert self.connection
        self.info("Shutting down socket %s", self.connection.fileno())
        self.connection.shutdown(socket.SHUT_RDWR)
        self.connection.close()
