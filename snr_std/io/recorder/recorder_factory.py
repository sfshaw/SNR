from typing import List

from snr_core.endpoint.endpoint import Endpoint
from snr_core.endpoint.reloadable_factory import ReloadableEndpointFactory
from snr_core.node import Node
from snr_std.io.recorder import recorder_endpoint


class RecorderFactory(ReloadableEndpointFactory):
    def __init__(self, name: str, data_names: List[str]):
        super().__init__(recorder_endpoint, "recorder_factory")
        self.endpoint_name = name
        self.data_names = data_names

    def get(self, parent: Node) -> Endpoint:
        return recorder_endpoint.RecorderEndpoint(self,
                                                  parent,
                                                  self.endpoint_name,
                                                  self.data_names)

    def __repr__(self) -> str:
        return f"Recorder Factory (data_names: {self.data_names})"
