from typing import List

from snr.core import *
from snr.type_defs import *
from snr.interfaces import *

from . import stopwatch_endpoint


class StopwatchEndpointFactory(EndpointFactory):
    def __init__(self,
                 times: List[float],
                 task_keys: List[TaskId],
                 ) -> None:
        super().__init__(stopwatch_endpoint)
        self.times = times
        self.task_keys = task_keys

    def get(self, parent: AbstractNode) -> AbstractEndpoint:
        return stopwatch_endpoint.StopwatchEndpoint(self,
                                                    parent,
                                                    self.times,
                                                    self.task_keys)
