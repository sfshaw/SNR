from multiprocessing.connection import Connection as MPConnection

from snr.core.base import *

from . import pipe_loop
from .pipe_wrapper import PipeWrapper


class PipeLoopFactory(LoopFactory):
    def __init__(self,
                 pipe: MPConnection,
                 data_keys: List[DataKey] = [],
                 ) -> None:
        super().__init__(pipe_loop)
        self.pipe = PipeWrapper(pipe)
        self.data_keys = data_keys

    def get(self, parent: NodeProtocol) -> LoopProtocol:
        return pipe_loop.PipeLoop(self, parent, self.pipe, self.data_keys)
