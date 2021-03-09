from multiprocessing.connection import Connection as MPConnection
from typing import List

from snr.core import *
from snr.protocol import *
from snr.type_defs import *

from ..comms_base import comms_loop
from . import pipe_wrapper


class PipeLoopFactory(LoopFactory):
    def __init__(self,
                 pipe: MPConnection,
                 data_keys: List[DataKey] = [],
                 ) -> None:
        super().__init__(pipe_wrapper)
        self.pipe = pipe
        self.data_keys = data_keys

    def get(self, parent: NodeProtocol) -> LoopProtocol:
        return comms_loop.CommsLoop(self,
                                    parent,
                                    "pipe_loop",
                                    pipe_wrapper.PipeWrapper(self.pipe,
                                                             parent),
                                    self.data_keys)
