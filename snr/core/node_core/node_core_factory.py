from snr.prelude import *

from ..endpoints import EndpointFactory
from . import node_core_endpoint


class NodeCoreFactory(EndpointFactory):
    def __init__(self) -> None:
        super().__init__(node_core_endpoint)

    def get(self,
            parent: AbstractNode,
            ) -> node_core_endpoint.NodeCoreEndpoint:
        return node_core_endpoint.NodeCoreEndpoint(self, parent)
