from typing import List

from snr.core import *
from snr.interfaces import *
from snr.type_defs import *

from . import recorder_endpoint


class RecorderEndpointFactory(EndpointFactory):
    def __init__(self, filename: str, data_keys: List[DataKey]):
        super().__init__(recorder_endpoint)
        self.filename = filename
        self.data_keys = data_keys

    def get(self, parent: AbstractNode) -> AbstractEndpoint:
        return recorder_endpoint.RecorderEndpoint(self,
                                                  parent,
                                                  "recorder",
                                                  self.filename,
                                                  self.data_keys)

    def __repr__(self) -> str:
        return f"Recorder Factory (data_names: {self.data_keys})"
