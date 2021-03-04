from multiprocessing.connection import Connection as MPConnection

from snr.core.base import *
from snr.types import *


class PipeWrapper(Context, ConnectionProtocol):
    def __init__(self,
                 pipe: MPConnection,
                 parent: ContextProtocol,
                 ) -> None:
        super().__init__("pipe_wrapper", parent.settings, parent.profiler)
        self.pipe = pipe

    def open(self) -> None:
        pass

    def is_closed(self) -> bool:
        return self.pipe.closed

    def send(self, data: bytes) -> None:
        self.pipe.send(data)

    def poll(self, timeout_ms: float) -> bool:
        return self.pipe.poll(timeout_ms)

    def recv(self) -> Optional[JsonData]:
        return self.pipe.recv()

    def close(self) -> None:
        self.pipe.close()
