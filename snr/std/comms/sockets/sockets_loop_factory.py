import socket

from snr.core.base import *

from ..comms_loop.comms_loop import CommsLoop
from . import sockets_wrapper


class SocketsLoopFactory(LoopFactory):
    def __init__(self,
                 connection: Tuple[socket.socket, Any],
                 data_keys: List[str],
                 ) -> None:
        super().__init__(sockets_wrapper)
        self.connection = connection
        self.data_keys = data_keys

    def get(self, parent: NodeProtocol) -> ThreadLoop:
        return CommsLoop(self,
                         parent,
                         "sockets_loop",
                         sockets_wrapper.SocketsWrapper(self.connection,
                                                        parent),
                         self.data_keys)
