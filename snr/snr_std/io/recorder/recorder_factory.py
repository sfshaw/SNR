from snr.snr_core.base import *

from . import recorder_endpoint


class RecorderFactory(EndpointFactory):
    def __init__(self, filename: str, data_keys: List[DataKey]):
        super().__init__(recorder_endpoint)
        self.filename = filename
        self.data_keys = data_keys

    def get(self, parent: NodeProtocol) -> EndpointProtocol:
        return recorder_endpoint.RecorderEndpoint(self,
                                                  parent,
                                                  "recorder",
                                                  self.filename,
                                                  self.data_keys)

    def __repr__(self) -> str:
        return f"Recorder Factory (data_names: {self.data_keys})"
