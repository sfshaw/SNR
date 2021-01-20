from typing import List

from snr_core.endpoint import EndpointBase
from snr_core.endpoint.reloadable_factory import ReloadableEndpointFactory
from snr.io.recorder import recorder
from snr_core.node import Node


class RecorderFactory(ReloadableEndpointFactory):
    def __init__(self, name: str, data_names: List[str]):
        super().__init__(recorder, "recorder_factory")
        self.endpoint_name = name
        self.data_names = data_names

    def get(self, parent: Node) -> EndpointBase:
        return recorder.Recorder(self,
                                 parent,
                                 self.endpoint_name,
                                 self.data_names)

    def __repr__(self) -> str:
        return f"Recorder Factory (data_names: {self.data_names})"
