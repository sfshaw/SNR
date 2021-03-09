import logging
import queue
import select
import socket
from typing import Any, List, Optional, Tuple

from snr.core import *
from snr.protocol import *
from snr.type_defs import *

from .sockets_loop_factory import SocketsLoopFactory

TIMEOUT_S: float = 0.001

HANDLE_CONNECTION_TASK_NAME: str = "handle_socket_connection"


class SocketsListenerLoop(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent: NodeProtocol,
                 name: str,
                 port: int,
                 data_keys: List[DataKey],
                 existing_socket: Optional[socket.socket] = None,
                 ) -> None:
        super().__init__(factory, parent, name)
        self.port = port
        self.data_keys = data_keys
        self.socket = existing_socket
        self.select = select.poll()
        self.handler_que: queue.Queue[Tuple[socket.socket, Any]] = queue.Queue(
        )
        self.task_handlers = {
            (TaskType.event, HANDLE_CONNECTION_TASK_NAME):
                self.handle_connection
        }
        self.log.setLevel(logging.WARNING)

    def setup(self):
        if self.socket:
            self.info("Socket already open")
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.settimeout(TIMEOUT_S)
            self.socket.bind(('', self.port))
            self.socket.listen(10)
        self.select.register(self.socket.fileno(), select.POLLIN)
        self.factory.existing_socket = self.socket  # type: ignore
        self.dbg("Socket server on fd(%s) ready", self.socket.fileno())

    def loop_handler(self) -> None:
        assert self.socket
        try:
            poll_result = self.select.poll(TIMEOUT_S)
            if ((len(poll_result) > 0) and
                    (poll_result[0] == (self.socket.fileno(), select.POLLIN))):
                self.dbg("Socket %s polled, blocking on accept",
                         self.socket.fileno())
                connection = self.socket.accept()
                self.handler_que.put(connection)
                self.parent.schedule(task_event(HANDLE_CONNECTION_TASK_NAME))
        except socket.timeout:
            pass

    def handle_connection(self, t: Task, k: TaskId) -> None:
        connection = self.handler_que.get_nowait()
        name = self.parent.add_component(SocketsLoopFactory(connection,
                                                            self.data_keys))
        if name:
            self.parent.endpoints[name].start()
            self.dbg("Added sockets loop to handle connection")
        else:
            self.err("Failed to add sockets_loop to parent node")

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        assert self.socket
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        self.dbg("Closed server socket")
