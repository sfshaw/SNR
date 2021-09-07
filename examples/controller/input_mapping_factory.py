from snr import *

import input_mapping_endpoint


class InputMappingFactory(EndpointFactory):

    input_data: DataKey
    output_data: DataKey

    def __init__(self,
                 input_data: DataKey = "raw_controller_input",
                 output_data: DataKey = "controller_input",
                 ) -> None:
        super().__init__(input_mapping_endpoint)
        self.input_data = input_data
        self.output_data = output_data

    def get(self, parent: AbstractNode) -> Endpoint:
        return input_mapping_endpoint.InputMappingEndpoint(self,
                                                           parent,
                                                           self.input_data,
                                                           self.output_data)
