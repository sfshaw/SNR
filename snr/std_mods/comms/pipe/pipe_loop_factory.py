from typing import List
from multiprocessing import connection
from snr.core import *
from snr.interfaces import *
from snr.type_defs import *

from ..comms_base import comms_loop
from . import pipe_wrapper


class PipeLoopFactory(LoopFactory):
    def __init__(self,
                 pipe: connection.Connection,
                 data_keys: List[DataKey] = [],
                 ) -> None:
        super().__init__(pipe_wrapper)
        self.pipe = pipe
        self.data_keys = data_keys

    def get(self, parent: AbstractNode) -> AbstractLoop:
        return comms_loop.CommsLoop(self,
                                    parent,
                                    "pipe_loop",
                                    pipe_wrapper.PipeWrapper(self.pipe,
                                                             parent),
                                    self.data_keys)
