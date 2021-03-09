from snr.protocol import *
from snr.type_defs import *

from . import node_core_endpoint
from .endpoint_factory import EndpointFactory


class NodeCoreFactory(EndpointFactory):
    def __init__(self) -> None:
        super().__init__(node_core_endpoint)

    def get(self, parent: NodeProtocol) -> EndpointProtocol:
        return node_core_endpoint.NodeCoreEndpoint(self, parent)
