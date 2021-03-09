import logging
import select
import socket
from typing import Any, List, Optional, Tuple

from snr.core import *
from snr.protocol import *
from snr.type_defs import *

from . import sockets_header


class SocketsWrapper(Context, ConnectionProtocol):

    def __init__(self,
                 connection: Tuple[socket.socket, Any],
                 parent: ContextProtocol,
                 ) -> None:
        super().__init__("sockets_wrapper",
                         parent.settings,
                         parent.profiler,
                         parent.timer)
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
        self.dbg("Sock %s: sent payload of size %s:\n%s",
                 self.connection.fileno(),
                 sockets_header.unpack_size(header),
                 data.decode())

    def poll(self, timeout_s: float = 0) -> bool:
        assert self.connection
        result: List[Tuple[int, int]] = self.select.poll(timeout_s * 1000)
        ready = ((len(result) > 0) and
                 (result[0] == (self.connection.fileno(),
                                select.POLLIN)))
        if ready:
            self.dbg("Ran poll on %s: %s => ready",
                     self.connection.fileno(),
                     result)
        return ready

    def recv(self) -> Optional[JsonData]:
        assert self.connection
        try:
            data_len = sockets_header.unpack_size(
                self.connection.recv(sockets_header.PACKET_SIZE_HEADER_LENGTH))
            self.dbg("Received header for %s bytes on sock %s",
                     data_len,
                     self.connection.fileno())
            data = self.connection.recv(data_len)
            self.dbg("Recevied %s bytes of data on %s",
                     len(data),
                     self.connection.fileno())
            return data
        except Exception as e:
            self.warn("Error in Recv: %s", e.__repr__())
            return None

    def close(self) -> None:
        assert self.connection
        self.info("Shutting down socket %s", self.connection.fileno())

        self.connection.detach()
        # try:
        #     self.connection.shutdown(socket.SHUT_RDWR)
        # except OSError as e:
        #     if e.errno in [107, 9]:
        #         # Socket is already closed
        #         pass
        #     else:
        #         raise e
