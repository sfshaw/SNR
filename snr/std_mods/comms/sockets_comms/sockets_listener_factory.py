import socket
from typing import List, Optional, Tuple, Union

from snr.core import *
from snr.interfaces import *
from snr.std_mods.comms.sockets_base import sockets_wrapper
from snr.type_defs import *

from . import sockets_listener_loop


class SocketsListenerFactory(LoopFactory):
    def __init__(self,
                 connection_or_port: Union[Tuple[socket.socket, int], int],
                 data_keys: List[DataKey] = [],
                 loop_name: ComponentName = "sockets_listener_loop",
                 ) -> None:
        super().__init__([
            sockets_listener_loop,
            sockets_wrapper,
        ])

        self.existing_socket: Optional[socket.socket] = None
        if isinstance(connection_or_port, int):
            self.port: int = connection_or_port
        else:
            self.existing_socket = connection_or_port[0]
            self.port = connection_or_port[1]
        self.data_keys = data_keys
        self.loop_name = loop_name

    def get(self, parent: AbstractNode) -> AbstractLoop:
        return sockets_listener_loop.SocketsListenerLoop(self,
                                                         parent,
                                                         self.loop_name,
                                                         self.port,
                                                         self.data_keys,
                                                         self.existing_socket)
