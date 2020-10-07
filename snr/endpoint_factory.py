from typing import List

from snr.endpoint import Endpoint
from snr.factory import EndpointFactory


class EndpointFactory(EndpointFactory):
    def __init__(self):
        pass

    def get(self, parent_node=None):
        return self.get_endpoints(parent_node)

    def get_endpoints(self, parent_node=None) -> List[Endpoint]:
        raise NotImplementedError
