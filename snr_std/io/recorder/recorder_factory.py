from typing import List

from snr_core.base import *
from snr_std.io.recorder import recorder_endpoint


class RecorderFactory(EndpointFactory):
    def __init__(self, filename: str, data_names: List[str]):
        super().__init__(recorder_endpoint, "recorder_factory")
        self.filename = filename
        self.data_names = data_names

    def get(self, parent: NodeProtocol) -> EndpointProtocol:
        return recorder_endpoint.RecorderEndpoint(self,
                                                  parent,
                                                  "recorder",
                                                  self.filename,
                                                  self.data_names)

    def __repr__(self) -> str:
        return f"Recorder Factory (data_names: {self.data_names})"
