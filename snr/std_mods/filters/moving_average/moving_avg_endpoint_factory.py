import collections
from typing import Deque

from snr.core import *
from snr.core.utils import moving_avg_filter

from . import moving_avg_endpoint

DEFAULT_FILTER_LENGTH: int = 3


class MovingAvgEndpointFactory(EndpointFactory):
    def __init__(self,
                 input: DataKey,
                 output: DataKey,
                 length: int,
                 endpoint_name: str = "moving_avg_filter",
                 ) -> None:
        super().__init__([moving_avg_endpoint, moving_avg_filter])
        self.input = input
        self.output = output
        self.backing_deque: Deque[float] = collections.deque(maxlen=length)
        self.endpoint_name = endpoint_name

    def get(self,
            parent: NodeProtocol,
            ) -> moving_avg_endpoint.MovingAvgEndpoint:
        filter = moving_avg_filter.MovingAvgFilter(self.backing_deque)
        return moving_avg_endpoint.MovingAvgEndpoint(self,
                                                     parent,
                                                     self.endpoint_name,
                                                     self.input,
                                                     self.output,
                                                     filter)
