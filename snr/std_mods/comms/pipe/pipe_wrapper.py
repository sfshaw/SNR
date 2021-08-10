import multiprocessing as mp
from typing import Optional

from snr.core import *
from snr.interfaces import *
from snr.type_defs import *


class PipeWrapper(Context, AbstractConnection):

    pipe: mp.connection.Connection

    def __init__(self,
                 pipe: mp.connection.Connection,
                 parent: AbstractContext,
                 ) -> None:
        super().__init__("pipe_wrapper",
                         parent.profiler,
                         parent.timer)
        self.pipe = pipe

    def open(self) -> None:
        pass

    def is_closed(self) -> bool:
        return self.pipe.closed

    def send(self, data: bytes) -> None:
        self.pipe.send(data)

    def poll(self, timeout_s: float) -> bool:
        return self.pipe.poll(timeout_s)

    def recv(self) -> Optional[JsonData]:
        return self.pipe.recv()

    def close(self) -> None:
        self.pipe.close()
