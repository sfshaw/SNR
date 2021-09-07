from typing import List, Tuple

from ....core import *
from ....prelude import *
from . import sockets_client_endpoint


class SocketsClientFactory(EndpointFactory):

    server_tuple: Tuple[str, int]
    keys: List[DataKey]

    def __init__(self,
                 server_tuple: Tuple[str, int],
                 keys: List[DataKey],
                 ) -> None:
        super().__init__(sockets_client_endpoint)
        self.server_tuple = server_tuple
        self.keys = keys

    def get(self, parent: AbstractNode) -> Endpoint:
        return sockets_client_endpoint.SocketsClientEndpoint(self,
                                                             parent,
                                                             self.server_tuple,
                                                             self.keys)
