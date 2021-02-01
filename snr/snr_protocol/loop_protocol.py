from snr.snr_protocol.endpoint_protocol import EndpointProtocol
from snr.snr_types import *


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

    def terminate(self) -> None:
        ...

    def is_terminated(self) -> bool:
        ...
