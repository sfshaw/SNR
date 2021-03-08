from snr.type_defs import *
from typing_extensions import Protocol, runtime_checkable

from .endpoint_protocol import EndpointProtocol


@runtime_checkable
class LoopProtocol(EndpointProtocol, Protocol):
    """An Asynchronous endpoint of data for a node

    An AsyncEndpoint is part of a node, and runs in its own thread. An
    endpoint may produce data to be stored in the Node or retreive data from
    the Node. The endpoint has its loop handler function run according to its
    tick_rate (Hz).
    """

    def setup(self) -> None:
        ...

    def loop_handler(self) -> None:
        ...

    def is_terminated(self) -> bool:
        ...
