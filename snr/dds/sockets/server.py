""" Sockets server for DDS
"""
import pickle
import socket
from socket import socket as Socket
from typing import Optional

from snr.dds.page import InboundStoreFn, Page
from snr.dds.sockets.config import SocketsConfig
from snr.endpoint.async_endpoint import AsyncEndpoint
from snr.node import Node


class SocketsServer(AsyncEndpoint):
    """Asynchronous sockets server which sends commands to robot
    """

    def __init__(self,
                 parent: Node,
                 config: SocketsConfig,
                 inbound_store: InboundStoreFn
                 ) -> None:
        super().__init__(parent,
                         name="dds_sockets_server",
                         loop_handler=self.receive_data,
                         tick_rate_hz=0)
        self.config: SocketsConfig = config
        self.inbound_store: InboundStoreFn = inbound_store

        self.s: Optional[Socket] = None
        self.ready: bool = False
        self.connected: bool = False

        # Async endpoint thread loop
        self.start_loop()

    def receive_data(self) -> None:
        self.diagnose()
        self.info("Waiting to receive data")
        try:
            assert isinstance(self.s, Socket)
            data = self.s.recv(self.settings.MAX_SOCKET_SIZE)
            self.dbg("Received data: {}", [data])
            page: Page = pickle.loads(data)
            self.inbound_store(page)
        except (ConnectionResetError, Exception) as error:
            self.err("Lost {} sockets connection: {}",
                     [self.name, error.__repr__()])

    def diagnose(self):
        if (not self.s) or (not self.ready):
            self.__init_socket()
        if not self.connected:
            self.__connect()

    def __init_socket(self):
        if self.s is not None:
            self.__close()

        # Create socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.settimeout(self.settings.SOCKETS_SERVER_TIMEOUT)

        # Bind to the socket
        try:
            host_tuple = self.config.tuple()
            self.s.bind(host_tuple)
            self.info("Socket bound to {}", [host_tuple])
        except socket.error as socket_error:
            self.fatal("Bind failed: {}", [socket_error])
            self.s.close()
            self.sleep(self.settings.SOCKETS_RETRY_WAIT)
        # Listen for connections
        try:
            self.s.listen(self.settings.SOCKETS_MAX_CONNECTIONS)
            self.info("Server now listening")
        except Exception as error:
            self.err("Error listening: {}",
                     [error.__repr__()])
            self.s.close()
            return
        self.ready = True
        self.connected = False

    def __connect(self):
        # Create connection to the client
        try:
            assert isinstance(self.s, Socket)
            # Blocking call waiting for the client to connect
            self.info("Blocking on accept_connection for {}",
                      [self.name])
            self.conn, self.addr = self.s.accept()
            self.connected = True
            return
        except (socket.timeout, OSError, Exception) as err:
            if isinstance(err, socket.timeout):
                self.dbg("Restarting sockets server after idle timeout")
            else:
                self.dbg("Connection failed: {}", [err.__repr__()])
            self.connected = False

    def __close(self):
        # if not settings.USE_SOCKETS:
        #     return
        try:
            if isinstance(self.s, Socket):
                self.s.close()
            self.s = None
            self.ready = False
            self.connected = False
        except Exception as error:
            self.err("Error closing socket: {}",
                     [error.__repr__()])

    def terminate(self):
        self.__close()
        self.warn("Socket closed")
