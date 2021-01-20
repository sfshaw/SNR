from __future__ import annotations
from typing import Any

from snr_core.context.context import Context

DEFAULT_TICK_RATE = 24
JOIN_TIMEOUT = None


class LoopBase(Context):
    """An Asynchronous endpoint of data for a node

    An AsyncEndpoint is part of a node, and runs in its own thread. An
    endpoint may produce data to be stored in the Node or retreive data from
    the Node. The endpoint has its loop handler function run according to its
    tick_rate (Hz).
    """

    def __init__(self,
                 parent_node: Any,
                 name: str,
                 ) -> None:
        super().__init__(name, parent_node)
        self.parent_node = parent_node

    def set_delay(self, tick_rate_hz: float) -> None:
        raise NotImplementedError

    def start(self) -> None:
        raise NotImplementedError

    def join(self) -> None:
        raise NotImplementedError

    def tick(self) -> None:
        raise NotImplementedError

    def is_terminated(self) -> bool:
        raise NotImplementedError

    def set_terminate_flag(self) -> None:
        raise NotImplementedError

    def terminate(self) -> None:
        raise NotImplementedError
