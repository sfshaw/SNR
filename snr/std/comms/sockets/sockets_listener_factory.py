from snr.core.base import *

from . import sockets_listener_loop


class SocketsListenerFactory(LoopFactory):
    def __init__(self,
                 port: int,
                 data_keys: List[DataKey] = [],
                 ) -> None:
        super().__init__(sockets_listener_loop)
        self.port = port
        self.data_keys = data_keys

    def get(self, parent: NodeProtocol) -> ThreadLoop:
        return sockets_listener_loop.SocketsListenerLoop(self,
                                                         parent,
                                                         self.port,
                                                         self.data_keys)
