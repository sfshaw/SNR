from snr_core.endpoint.endpoint import Endpoint
from snr_core.endpoint.endpoint_factory import EndpointFactory
from snr_core.node import Node
from snr_std.kalman import kalman_endpoint


class KalmanFilterFactory(EndpointFactory):
    def __init__(self,
                 input_data_name: str,
                 output_data_name: str
                 ) -> None:
        super().__init__("Kalman Kilter Endpoint Factory")
        self.input_data_name = input_data_name
        self.output_data_name = output_data_name

    def get(self, parent: Node) -> Endpoint:
        return kalman_endpoint.KalmanEndpoint(self,
                                              parent,
                                              "kalman_filter_endpoint",
                                              self.input_data_name,
                                              self.output_data_name)
