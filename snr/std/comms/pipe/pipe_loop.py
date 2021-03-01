from snr.core.base import *
from snr.std.comms.pipe.pipe_wrapper import PipeWrapper

from ..comms_loop.comms_loop import CommsLoopBase

POLL_TIMEOUT = 0.000001


class PipeLoop(CommsLoopBase):
    def __init__(self,
                 factory: LoopFactory,
                 parent: NodeProtocol,
                 pipe: PipeWrapper,
                 data_keys: List[DataKey],
                 ) -> None:
        super().__init__(factory, parent, "pipe_loop", pipe, data_keys)
        self.task_handlers: TaskHandlerMap = {}
        for key in data_keys:
            self.task_handlers[(TaskType.process_data, key)
                               ] = self.process_data

    def setup(self) -> None:
        pass

    def terminate(self) -> None:
        self.connection.close()
