from snr.core import *
from snr.interfaces import *

from . import kalman_endpoint


class KalmanFilterFactory(EndpointFactory):
    def __init__(self,
                 input_data_name: str,
                 output_data_name: str
                 ) -> None:
        super().__init__(kalman_endpoint)
        self.input_data_name = input_data_name
        self.output_data_name = output_data_name

    def get(self, parent: AbstractNode) -> AbstractEndpoint:
        return kalman_endpoint.KalmanEndpoint(self,
                                              parent,
                                              "kalman_filter_endpoint",
                                              self.input_data_name,
                                              self.output_data_name)
