from snr_core.endpoint.synchronous_endpoint import Endpoint
from snr_core.endpoint.endpoint_factory import EndpointFactory
from snr_core.node import Node

from snr.io.controller.controller import Controller


class ControllerFactory(EndpointFactory):
    def __init__(self, output_data_name: str):
        super().__init__("Controller Factory")
        self.output_data_name = output_data_name

    def get(self, parent: Node) -> Endpoint:
        return Controller(parent, self.output_data_name)

    def __repr__(self):
        return "Controller Factory"
