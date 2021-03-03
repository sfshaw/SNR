import socket
import threading
from socket import socket as Socket

from snr.core.base import *

LOCALHOST = "localhost"
MAX_CONNECTIONS = 10


class DiscoveryServer(Context):
    def __init__(self, parent: ContextProtocol, role: str, port: int):
        super().__init__("discovery_server", parent.settings, parent.profiler)
        self.role = role
        self.port = port
        self.host_tuple = (LOCALHOST, port)
        self.s: Optional[Socket] = None
        self.__init_socket()
        self.terminate_flag = self.s is None
        self.thread = threading.Thread(target=self.loop,
                                       args=[])
        self.thread.start()

    def loop(self):
        while not self.terminate_flag:
            self.__handle_connection()
        self.__shutdown()

    def terminate(self):
        self.terminate_flag = True
        self.thread.join(1)
        self.__shutdown()

    def __shutdown(self):
        self.terminate_flag = True
        if self.s:
            self.s.close()
            self.s = None

    def __init_socket(self):
        if self.s is not None:
            self.s.close()

        # Create socket
        self.s = Socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.s.settimeout(settings.SOCKETS_SERVER_TIMEOUT)

        # Bind to the socket
        try:
            self.s.bind(self.host_tuple)
            self.info("Server socket bound to {}:{}",
                      [self.host_tuple[0], self.host_tuple[1]])
        except socket.error as socket_error:
            self.err("Bind failed: {}", [socket_error])
            self.__shutdown()
            # time.sleep(self.settings.SOCKETS_RETRY_WAIT_S)
        # Listen for connections
        try:
            self.s.listen(MAX_CONNECTIONS)
            self.info("Server now listening")
        except Exception as error:
            self.err("Error listening: {}",
                     [error.__repr__()])
            self.__shutdown()
            return

    def __handle_connection(self):
        # Create connection to the client
        try:
            assert isinstance(self.s, Socket)
            # Blocking call waiting for the client to connect
            self.info("Blocking on accept_connection")
            conn, addr = self.s.accept()
            encoded_data = self.role.encode()
            self.dbg("Providing name: {} to {}",
                     [encoded_data, addr])
            conn.sendall(encoded_data)
            conn.close()
            return
        except (socket.timeout, OSError, Exception) as e:
            if isinstance(e, socket.timeout):
                self.info("Restarting sockets server after idle timeout")
            else:
                self.warn("Connection failed: {}", [e])
