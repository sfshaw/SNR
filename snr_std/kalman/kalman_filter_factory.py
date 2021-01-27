from snr_core.base import *
from snr_std.kalman import kalman_endpoint


class KalmanFilterFactory(EndpointFactory):
    def __init__(self,
                 input_data_name: str,
                 output_data_name: str
                 ) -> None:
        super().__init__(kalman_endpoint, "Kalman Kilter Endpoint Factory")
        self.input_data_name = input_data_name
        self.output_data_name = output_data_name

    def get(self, parent: Node) -> EndpointProtocol:
        return kalman_endpoint.KalmanEndpoint(self,
                                              parent,
                                              "kalman_filter_endpoint",
                                              self.input_data_name,
                                              self.output_data_name)
