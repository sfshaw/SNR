import logging
import select
import socket
from typing import List, Optional

from snr.core import *
from snr.interfaces import *
from snr.type_defs import *

from .sockets_loop_factory import SocketsLoopFactory

SOCK_TIMEOUT_S: float = 0.000010
POLL_TIMEOUT_MS: float = 0


class SocketsListenerLoop(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent: AbstractNode,
                 name: ComponentName,
                 port: int,
                 data_keys: List[DataKey],
                 existing_socket: Optional[socket.socket] = None,
                 ) -> None:
        super().__init__(factory, parent, name)
        self.log.setLevel(logging.WARNING)
        self.port = port
        self.data_keys = data_keys
        self.socket = existing_socket
        self.select = select.poll()

    def setup(self):
        if self.socket:
            self.info("Socket already open")
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.settimeout(SOCK_TIMEOUT_S)
            self.socket.bind(('', self.port))
            self.socket.listen(10)
        self.select.register(self.socket.fileno(), select.POLLIN)
        self.factory.existing_socket = self.socket  # type: ignore
        self.dbg("Socket server on fd(%s) ready", self.socket.fileno())

    def loop(self) -> None:
        assert self.socket
        try:
            poll_result = self.select.poll(POLL_TIMEOUT_MS)
            if ((len(poll_result) > 0) and
                    (poll_result[0] == (self.socket.fileno(), select.POLLIN))):
                self.dbg("Socket %s polled, blocking on accept",
                         self.socket.fileno())
                connection = self.socket.accept()
                self.dbg("Scheduling add_component to handle connection")
                self.schedule(tasks.add_component(
                    SocketsLoopFactory(connection,
                                       self.data_keys)))
        except socket.timeout:
            pass

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        assert self.socket
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        self.dbg("Closed server socket")
