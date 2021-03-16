from snr.core import *
from snr.interfaces import *
from snr.type_defs import *

from . import kalman_endpoint


class KalmanFilterFactory(EndpointFactory):
    def __init__(self,
                 input_data_key: DataKey,
                 output_data_key: DataKey
                 ) -> None:
        super().__init__(kalman_endpoint)
        self.input_data_key = input_data_key
        self.output_data_key = output_data_key

    def get(self, parent: AbstractNode) -> AbstractEndpoint:
        return kalman_endpoint.KalmanEndpoint(self,
                                              parent,
                                              "kalman_filter_endpoint",
                                              self.input_data_key,
                                              self.output_data_key)
