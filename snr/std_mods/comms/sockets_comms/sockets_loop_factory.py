'''Factory class for injecting a sockets wrapper into a CommsLoop

Since this factory uses `snr.core.utils.sockets.sockets_wrapper` as its child
module, the wrapper moduel is reloaded instead of
`snr.std_mods.comms.comms_loop.CommsLoop`.
'''

import socket
from typing import Any, List, Tuple, Union

from snr.core import *
from snr.protocol import *
from snr.std_mods.comms.comms_base import comms_loop
from snr.std_mods.comms.sockets_base import sockets_wrapper
from snr.type_defs import *


class SocketsLoopFactory(LoopFactory):

    def __init__(self,
                 connection: Tuple[socket.socket, Any],
                 data_keys: List[str],
                 ) -> None:
        super().__init__(sockets_wrapper)
        self.connection: Union[Tuple[socket.socket, Any],
                               ConnectionProtocol] = connection
        self.data_keys = data_keys

    def get(self, parent: NodeProtocol) -> ThreadLoop:
        if not isinstance(self.connection, ConnectionProtocol):
            self.connection = sockets_wrapper.SocketsWrapper(
                self.connection,
                parent)
        assert isinstance(self.connection, ConnectionProtocol)
        return comms_loop.CommsLoop(self,
                                    parent,
                                    "sockets_loop",
                                    self.connection,
                                    self.data_keys)
