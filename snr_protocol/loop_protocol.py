from snr_types import *

from snr_protocol.component_protocol import ComponentProtocol


@runtime_checkable
class LoopProtocol(ComponentProtocol, Protocol):
    """An Asynchronous endpoint of data for a node

    An AsyncEndpoint is part of a node, and runs in its own thread. An
    endpoint may produce data to be stored in the Node or retreive data from
    the Node. The endpoint has its loop handler function run according to its
    tick_rate (Hz).
    """

    def start(self) -> None:
        ...

    def join(self) -> None:
        ...

    def setup(self) -> None:
        ...

    def loop_handler(self) -> None:
        ...

    def terminate(self) -> None:
        ...

    def is_terminated(self) -> bool:
        ...

    def set_terminate_flag(self) -> None:
        ...
