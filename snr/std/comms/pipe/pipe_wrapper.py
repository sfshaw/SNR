from multiprocessing.connection import Connection as MPConnection

from snr.types import *

from ..comms_loop.connection import Connection


class PipeWrapper(Connection):
    def __init__(self, pipe: MPConnection) -> None:
        self.pipe = pipe

    def open(self) -> None:
        pass

    def is_closed(self) -> bool:
        return self.pipe.closed

    def send(self, data: str) -> None:
        self.pipe.send(data)

    def poll(self, timeout_ms: float) -> bool:
        return self.pipe.poll(timeout_ms)

    def recv(self) -> Optional[str]:
        return self.pipe.recv()

    def close(self) -> None:
        self.pipe.close()
