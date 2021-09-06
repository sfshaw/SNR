from typing import List, Tuple

from ....core import *
from ....prelude import *
from .sockets_client_factory import SocketsClientFactory
from .sockets_listener_factory import SocketsListenerFactory


class SocketsPair:

    server_tuple: Tuple[str, int]
    port: int

    def __init__(self, server_tuple: Tuple[str, int]) -> None:
        self.server_tuple = server_tuple

    def client(self, keys: List[DataKey]) -> EndpointFactory:
        return SocketsClientFactory(self.server_tuple, keys)

    def server(self) -> LoopFactory:
        return SocketsListenerFactory(self.server_tuple[1])
