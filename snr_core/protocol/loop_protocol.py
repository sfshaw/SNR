from __future__ import annotations

from typing import Protocol, runtime_checkable

from snr_core.protocol.component_protocol import Component

DEFAULT_TICK_RATE = 24
JOIN_TIMEOUT = None


@runtime_checkable
class LoopProtocol(Component, Protocol):
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

    def is_terminated(self) -> bool:
        ...

    def set_terminate_flag(self) -> None:
        ...
