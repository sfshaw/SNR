import logging
from typing import Optional

from snr.prelude import *


class Context(AbstractContext):

    def __init__(self,
                 name: str,
                 profiler: Optional[AbstractProfiler],
                 timer: TimerProtocol,
                 ) -> None:
        self.name = name
        self.log = logging.getLogger(self.name)
        self.profiler = profiler
        self.timer = timer
