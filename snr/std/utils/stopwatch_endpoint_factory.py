from snr.core.base import *

from . import stopwatch_endpoint


class StopwatchEndpointFactory(EndpointFactory):
    def __init__(self,
                 times: List[float]
                 ) -> None:
        super().__init__(stopwatch_endpoint)
        self.times = times

    def get(self, parent: NodeProtocol) -> EndpointProtocol:
        return stopwatch_endpoint.StopwatchEndpoint(self,
                                                    parent,
                                                    self.times)
