from snr.core.base import *

from . import pipe_loop
from .connection import Connection


class PipeLoopFactory(LoopFactory):
    def __init__(self,
                 pipe: Connection,
                 data_keys: List[DataKey] = [],
                 ) -> None:
        super().__init__(pipe_loop)
        self.pipe = pipe
        self.data_keys = data_keys

    def get(self, parent: NodeProtocol) -> LoopProtocol:
        return pipe_loop.PipeLoop(self, parent, self.pipe, self.data_keys)
