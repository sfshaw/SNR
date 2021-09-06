from snr import *

import control_processor_endpoint


class ControlProcessorFactory(EndpointFactory):

    input_data: DataKey

    def __init__(self,
                 input_data: DataKey = "controller_input",
                 ) -> None:
        super().__init__(control_processor_endpoint)
        self.input_data = input_data

    def get(self, parent: AbstractNode) -> Endpoint:
        return control_processor_endpoint.ControlProcessorEndpoint(
            self,
            parent,
            self.input_data)
