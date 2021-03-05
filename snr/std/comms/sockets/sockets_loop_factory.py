import socket

from snr.core.base import *
from snr.core.utils.sockets import sockets_wrapper

from .. import comms_loop


class SocketsLoopFactory(LoopFactory):
    def __init__(self,
                 connection: Tuple[socket.socket, Any],
                 data_keys: List[str],
                 ) -> None:
        super().__init__(sockets_wrapper)
        self.connection = connection
        self.data_keys = data_keys

    def get(self, parent: NodeProtocol) -> ThreadLoop:
        return comms_loop.CommsLoop(self,
                                    parent,
                                    "sockets_loop",
                                    sockets_wrapper.SocketsWrapper(
                                        self.connection,
                                        parent),
                                    self.data_keys)
